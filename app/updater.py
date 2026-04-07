"""
自动更新模块 — 对接 GitHub Releases API
工作流程：
  1. 启动时后台线程请求 GitHub API 获取最新 Release
  2. 比较版本号，若有新版本则通知主线程
  3. 用户确认后，后台下载安装包（从 Release Assets）
  4. 下载完成后，启动安装包（/VERYSILENT）并退出当前程序
"""

import json
import os
import re
import sys
import tempfile
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError

try:
    from packaging.version import Version, InvalidVersion
    _HAS_PACKAGING = True
except ImportError:
    _HAS_PACKAGING = False

from PySide6.QtCore import QThread, Signal, QObject, QTimer


# ══════════════════════════════════════════════════
#  配置 — 修改为你的 GitHub 仓库信息
# ══════════════════════════════════════════════════
GITHUB_OWNER = "zk-studio"        # ← 替换为你的 GitHub 用户名
GITHUB_REPO  = "batch-renamer"        # ← 替换为你的仓库名

# GitHub API 自动拼接，无需手动维护 URL
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"


# ── 版本比较工具 ──
def _version_tuple(ver_str: str) -> tuple:
    """将 '1.2.3' 转为 (1, 2, 3)"""
    parts = []
    for p in ver_str.strip().lstrip("v").split("."):
        try:
            parts.append(int(p))
        except ValueError:
            parts.append(0)
    return tuple(parts)


def _is_newer(remote: str, current: str) -> bool:
    """判断远程版本是否比当前版本新"""
    # 统一去掉 v 前缀
    remote = remote.lstrip("v")
    current = current.lstrip("v")

    if _HAS_PACKAGING:
        try:
            return Version(remote) > Version(current)
        except Exception:
            pass
    return _version_tuple(remote) > _version_tuple(current)


class UpdateInfo:
    """远程版本信息"""
    __slots__ = ("version", "download_url", "changelog", "mandatory")

    def __init__(self, version: str, download_url: str,
                 changelog: str = "", mandatory: bool = False):
        self.version = version
        self.download_url = download_url
        self.changelog = changelog
        self.mandatory = mandatory


# ═══════════════════════════════════════════════
#  检查更新线程 — 直接读取 GitHub Releases API
# ═══════════════════════════════════════════════
class UpdateCheckWorker(QThread):
    """
    后台线程：请求 GitHub Releases API，解析最新版本。
    自动从 Release Assets 中找到 _Setup_*.exe 安装包。
    """
    update_available = Signal(object)   # UpdateInfo
    check_failed = Signal(str)          # 错误信息
    check_finished = Signal()

    def __init__(self, current_version: str, api_url: str = GITHUB_API_URL):
        super().__init__()
        self.current_version = current_version
        self.api_url = api_url

    def run(self):
        try:
            req = Request(self.api_url, headers={
                "User-Agent": "BatchRenamer-Updater",
                "Accept": "application/vnd.github.v3+json",
            })
            with urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            # 从 Release 中提取信息
            tag_name = data.get("tag_name", "")            # 例: "v1.1.0"
            remote_ver = tag_name.lstrip("v")               # 例: "1.1.0"
            changelog = data.get("body", "")                # Release Notes
            prerelease = data.get("prerelease", False)

            # 跳过预发布版本
            if prerelease:
                self.check_finished.emit()
                return

            # 从 Assets 中找安装包（优先 _Setup_*.exe）
            download_url = ""
            assets = data.get("assets", [])
            for asset in assets:
                name = asset.get("name", "")
                if name.endswith(".exe") and "Setup" in name:
                    download_url = asset.get("browser_download_url", "")
                    break

            # 如果没找到 Setup，尝试找任意 .exe
            if not download_url:
                for asset in assets:
                    if asset.get("name", "").endswith(".exe"):
                        download_url = asset.get("browser_download_url", "")
                        break

            if download_url and _is_newer(remote_ver, self.current_version):
                info = UpdateInfo(remote_ver, download_url, changelog)
                self.update_available.emit(info)
                return

        except URLError as e:
            self.check_failed.emit(f"网络错误: {e.reason}")
        except Exception as e:
            self.check_failed.emit(str(e))
        finally:
            self.check_finished.emit()


# ═══════════════════════════════════════════════
#  下载更新线程
# ═══════════════════════════════════════════════
class DownloadWorker(QThread):
    """
    后台线程：从 GitHub Release Assets 下载安装包到临时目录。
    """
    progress = Signal(int, int)            # (已下载字节, 总字节)
    download_finished = Signal(str)        # 本地文件路径
    download_failed = Signal(str)          # 错误信息

    def __init__(self, download_url: str):
        super().__init__()
        self.download_url = download_url

    def run(self):
        try:
            req = Request(self.download_url, headers={
                "User-Agent": "BatchRenamer-Updater",
            })
            with urlopen(req, timeout=120) as resp:
                total = int(resp.headers.get("Content-Length", 0))

                # 保存到临时目录
                tmp_dir = Path(tempfile.gettempdir()) / "BatchRenamer_Update"
                tmp_dir.mkdir(exist_ok=True)

                filename = self.download_url.split("/")[-1]
                if not filename.endswith(".exe"):
                    filename = "BatchRenamer_Setup_latest.exe"
                save_path = tmp_dir / filename

                downloaded = 0
                with open(save_path, "wb") as f:
                    while True:
                        chunk = resp.read(64 * 1024)  # 64KB chunks
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        self.progress.emit(downloaded, total)

            self.download_finished.emit(str(save_path))

        except Exception as e:
            self.download_failed.emit(str(e))


# ═══════════════════════════════════════════════
#  更新管理器 — 供 MainWindow 使用
# ═══════════════════════════════════════════════
class UpdateManager(QObject):
    """
    更新管理器：封装完整的 检查→提示→下载→安装 流程。
    直接对接 GitHub Releases API，无需自建服务器。

    使用方式:
        self.update_manager = UpdateManager(current_version="1.0.0")
        self.update_manager.update_available.connect(self._on_update_available)
        self.update_manager.start_check()
    """

    # 对外信号
    update_available = Signal(object)       # UpdateInfo
    download_progress = Signal(int, int)    # (已下载, 总大小)
    download_finished = Signal(str)         # 安装包路径
    download_failed = Signal(str)
    check_failed = Signal(str)
    no_update = Signal()

    def __init__(self, current_version: str, parent=None):
        super().__init__(parent)
        self.current_version = current_version
        self._check_worker: UpdateCheckWorker | None = None
        self._download_worker: DownloadWorker | None = None

    def start_check(self, delay_ms: int = 3000):
        """延迟 delay_ms 毫秒后开始检查更新（避免阻塞启动）"""
        QTimer.singleShot(delay_ms, self._do_check)

    def _do_check(self):
        self._check_worker = UpdateCheckWorker(self.current_version)
        self._check_worker.update_available.connect(self.update_available.emit)
        self._check_worker.check_failed.connect(self.check_failed.emit)
        self._check_worker.check_finished.connect(self.no_update.emit)
        self._check_worker.start()

    def start_download(self, download_url: str):
        """开始下载更新包"""
        self._download_worker = DownloadWorker(download_url)
        self._download_worker.progress.connect(self.download_progress.emit)
        self._download_worker.download_finished.connect(self.download_finished.emit)
        self._download_worker.download_failed.connect(self.download_failed.emit)
        self._download_worker.start()

    @staticmethod
    def install_and_quit(installer_path: str):
        """
        启动安装包（静默模式）并退出当前程序。
        Inno Setup 静默参数：
          /VERYSILENT        — 完全无界面
          /SUPPRESSMSGBOXES  — 不弹任何对话框
          /NORESTART         — 不重启电脑
          /CLOSEAPPLICATIONS — 自动关闭正在运行的旧版本
        """
        import subprocess
        cmd = [
            installer_path,
            "/VERYSILENT",
            "/SUPPRESSMSGBOXES",
            "/NORESTART",
            "/CLOSEAPPLICATIONS",
        ]
        subprocess.Popen(cmd, shell=False)
        from PySide6.QtWidgets import QApplication
        QApplication.quit()
