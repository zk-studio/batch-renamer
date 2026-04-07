"""
主窗口 — 组装各控件、连接信号、协调逻辑
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QColor
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QStatusBar, QProgressBar, QMessageBox,
)

from . import __version__, __app_name__
from .styles import STYLESHEET
from .rename_engine import RenameEngine
from .widgets import FolderSelector, RulePanel, PreviewTable
from .updater import UpdateManager


class MainWindow(QMainWindow):
    """批量文件重命名工具 — 主窗口"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"🔄  {__app_name__}")
        self.setMinimumSize(960, 700)
        self.resize(1080, 780)

        # 核心对象
        self.engine = RenameEngine()
        self.current_folder: str = ""
        self.file_list: list[str] = []

        # 构建 UI
        self._init_menu_bar()
        self._init_central()
        self._init_status_bar()

        # 应用样式
        self.setStyleSheet(STYLESHEET)
        self._center_window()

        # 启动自动更新检查（延迟 3 秒，不阻塞启动）
        self._init_updater()

    # ─────────── UI 初始化 ───────────

    def _center_window(self):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def _init_menu_bar(self):
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu("📁 文件")

        act_open = QAction("📂 选择文件夹", self)
        act_open.setShortcut("Ctrl+O")
        act_open.triggered.connect(self._on_select_folder_menu)
        file_menu.addAction(act_open)

        file_menu.addSeparator()

        act_exit = QAction("🚪 退出", self)
        act_exit.setShortcut("Ctrl+Q")
        act_exit.triggered.connect(self.close)
        file_menu.addAction(act_exit)

        # 编辑菜单
        edit_menu = menubar.addMenu("✏️ 编辑")

        act_undo = QAction("↩️ 撤销重命名", self)
        act_undo.setShortcut("Ctrl+Z")
        act_undo.triggered.connect(self._on_undo)
        edit_menu.addAction(act_undo)

        act_clear = QAction("🗑️ 清空列表", self)
        act_clear.triggered.connect(self._on_clear)
        edit_menu.addAction(act_clear)

        # 帮助菜单
        help_menu = menubar.addMenu("❓ 帮助")

        act_check_update = QAction("🔄 检查更新", self)
        act_check_update.triggered.connect(self._manual_check_update)
        help_menu.addAction(act_check_update)

        help_menu.addSeparator()

        act_about = QAction("💡 关于", self)
        act_about.triggered.connect(self._show_about)
        help_menu.addAction(act_about)

    def _init_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.status_label = QLabel("就绪 — 请选择一个文件夹开始")
        self.status_bar.addWidget(self.status_label, 1)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(200)
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)

        self.file_count_label = QLabel("")
        self.file_count_label.setObjectName("labelStats")
        self.status_bar.addPermanentWidget(self.file_count_label)

    def _init_central(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(20, 16, 20, 12)
        layout.setSpacing(14)

        # ── 标题区域 ──
        title_row = QHBoxLayout()
        title_col = QVBoxLayout()
        title_col.setSpacing(2)

        lbl_title = QLabel("⚡ 批量重命名工具")
        lbl_title.setObjectName("labelTitle")
        lbl_subtitle = QLabel("安全、快速地批量修改文件名")
        lbl_subtitle.setObjectName("labelSubtitle")

        title_col.addWidget(lbl_title)
        title_col.addWidget(lbl_subtitle)
        title_row.addLayout(title_col)
        title_row.addStretch()
        layout.addLayout(title_row)

        # ── 文件夹选择 ──
        self.folder_selector = FolderSelector()
        self.folder_selector.folderSelected.connect(self._on_folder_selected)
        layout.addWidget(self.folder_selector)

        # ── 重命名规则 ──
        self.rule_panel = RulePanel()
        self.rule_panel.paramsChanged.connect(self._refresh_preview)
        self.rule_panel.filter_edit.textChanged.connect(self._refresh_file_list)
        self.rule_panel.chk_subdirs.stateChanged.connect(self._refresh_file_list)
        layout.addWidget(self.rule_panel)

        # ── 预览表格 ──
        self.preview_table = PreviewTable()
        layout.addWidget(self.preview_table, 1)  # stretch=1 让表格占据剩余空间

        # ── 操作按钮 ──
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        btn_preview = QPushButton("🔍  刷新预览")
        btn_preview.setCursor(Qt.PointingHandCursor)
        btn_preview.clicked.connect(self._refresh_preview)

        self.btn_rename = QPushButton("✅  执行重命名")
        self.btn_rename.setObjectName("btnRename")
        self.btn_rename.setCursor(Qt.PointingHandCursor)
        self.btn_rename.setEnabled(False)
        self.btn_rename.clicked.connect(self._on_rename)

        self.btn_undo = QPushButton("↩️  撤销上次")
        self.btn_undo.setObjectName("btnUndo")
        self.btn_undo.setCursor(Qt.PointingHandCursor)
        self.btn_undo.setEnabled(False)
        self.btn_undo.clicked.connect(self._on_undo)

        btn_row.addStretch()
        btn_row.addWidget(btn_preview)
        btn_row.addWidget(self.btn_rename)
        btn_row.addWidget(self.btn_undo)
        layout.addLayout(btn_row)

    # ─────────── 信号槽 ───────────

    def _on_select_folder_menu(self):
        """菜单栏触发的文件夹选择"""
        self.folder_selector.btn_select.click()

    def _on_folder_selected(self, folder: str):
        """文件夹选择完成"""
        self.current_folder = folder
        self.status_label.setText(f"已加载：{folder}")
        self._refresh_file_list()

    def _refresh_file_list(self):
        """重新扫描文件"""
        if not self.current_folder:
            return

        self.file_list = RenameEngine.scan_files(
            self.current_folder,
            ext_filter=self.rule_panel.get_ext_filter(),
            include_subdirs=self.rule_panel.get_include_subdirs(),
        )
        self.file_count_label.setText(f"📄 {len(self.file_list)} 个文件")
        self._refresh_preview()

    def _refresh_preview(self):
        """刷新预览表格"""
        if not self.file_list:
            self.preview_table.clear()
            self.btn_rename.setEnabled(False)
            return

        params = self.rule_panel.get_params()
        preview_data = RenameEngine.compute_preview(self.file_list, params)
        self.preview_table.update_preview(preview_data)

        has_changes = any(changed for _, _, changed in preview_data)
        self.btn_rename.setEnabled(has_changes)
        self.status_label.setText(
            f"预览就绪 — {'有' if has_changes else '无'}变更  |  共 {len(self.file_list)} 个文件"
        )

    def _on_rename(self):
        """执行批量重命名"""
        if not self.file_list or not self.current_folder:
            return

        reply = QMessageBox.question(
            self, "确认重命名",
            f"即将重命名 {len(self.file_list)} 个文件。\n\n"
            "此操作可通过「撤销」按钮回退。\n确认继续？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return

        # 进度条
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # indeterminate
        QApplication.processEvents()

        params = self.rule_panel.get_params()
        result = self.engine.execute(self.current_folder, self.file_list, params)

        self.progress_bar.setVisible(False)
        self.btn_undo.setEnabled(self.engine.can_undo)

        # 结果提示
        msg = f"✅ 成功重命名 {result.success_count} 个文件"
        if result.errors:
            msg += f"\n\n⚠️ {len(result.errors)} 个文件出错：\n"
            msg += "\n".join(result.errors[:10])
            if len(result.errors) > 10:
                msg += f"\n… 还有 {len(result.errors) - 10} 个错误"

        QMessageBox.information(self, "重命名完成", msg)
        self.status_label.setText(
            f"✅ 已完成 — 成功 {result.success_count}，失败 {len(result.errors)}"
        )

        self._refresh_file_list()

    def _on_undo(self):
        """撤销上一次重命名"""
        if not self.engine.can_undo:
            QMessageBox.information(self, "撤销", "没有可撤销的操作。")
            return

        reply = QMessageBox.question(
            self, "确认撤销",
            "确定要撤销上一次重命名操作吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return

        result = self.engine.undo()
        self.btn_undo.setEnabled(self.engine.can_undo)

        msg = f"↩️ 已撤销 {result.success_count} 个文件"
        if result.errors:
            msg += f"\n\n⚠️ {len(result.errors)} 个文件回退失败：\n"
            msg += "\n".join(result.errors[:10])

        QMessageBox.information(self, "撤销完成", msg)
        self.status_label.setText(f"↩️ 已撤销 {result.success_count} 个文件的重命名")
        self._refresh_file_list()

    def _on_clear(self):
        """清空所有状态"""
        self.file_list = []
        self.current_folder = ""
        self.folder_selector.clear()
        self.preview_table.clear()
        self.btn_rename.setEnabled(False)
        self.file_count_label.setText("")
        self.status_label.setText("就绪 — 请选择一个文件夹开始")

    # ─────────── 自动更新 ───────────

    def _init_updater(self):
        """初始化更新管理器，延迟 3 秒检查 GitHub Releases"""
        self.update_manager = UpdateManager(
            current_version=__version__,
            parent=self,
        )
        self.update_manager.update_available.connect(self._on_update_available)
        self.update_manager.download_progress.connect(self._on_download_progress)
        self.update_manager.download_finished.connect(self._on_download_finished)
        self.update_manager.download_failed.connect(self._on_download_failed)
        self.update_manager.check_failed.connect(self._on_check_failed)

        # 延迟 3 秒开始检查
        self.update_manager.start_check(delay_ms=3000)

    def _manual_check_update(self):
        """菜单手动检查更新"""
        self.status_label.setText("🔄 正在检查更新…")
        self.update_manager.start_check(delay_ms=0)

    def _on_update_available(self, info):
        """发现新版本 → 弹窗询问"""
        changelog = info.changelog or "修复已知问题，提升性能。"
        msg = (
            f"发现新版本 v{info.version}！\n"
            f"当前版本 v{__version__}\n\n"
            f"📋 更新内容：\n{changelog}\n\n"
            "是否立即下载并安装？\n"
            "（安装过程将自动完成，无需手动操作）"
        )

        reply = QMessageBox.question(
            self, "🔔 发现新版本", msg,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes,
        )

        if reply == QMessageBox.Yes:
            self.status_label.setText("⬇️ 正在下载更新…")
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 100)
            self.progress_bar.setValue(0)
            self.update_manager.start_download(info.download_url)
        else:
            self.status_label.setText("已跳过更新")

    def _on_download_progress(self, downloaded: int, total: int):
        """下载进度回调"""
        if total > 0:
            pct = int(downloaded * 100 / total)
            self.progress_bar.setValue(pct)
            mb_done = downloaded / (1024 * 1024)
            mb_total = total / (1024 * 1024)
            self.status_label.setText(f"⬇️ 下载中 {mb_done:.1f} / {mb_total:.1f} MB")
        else:
            self.progress_bar.setRange(0, 0)  # indeterminate
            self.status_label.setText("⬇️ 下载中…")

    def _on_download_finished(self, installer_path: str):
        """下载完成 → 静默安装"""
        self.progress_bar.setVisible(False)
        self.status_label.setText("✅ 下载完成，正在启动安装…")

        QMessageBox.information(
            self, "更新就绪",
            "新版本已下载完成。\n\n"
            "点击确定后将自动关闭程序并静默安装。\n"
            "安装完成后请重新打开应用。",
        )

        # 启动静默安装并退出
        UpdateManager.install_and_quit(installer_path)

    def _on_download_failed(self, error: str):
        """下载失败"""
        self.progress_bar.setVisible(False)
        self.status_label.setText("❌ 更新下载失败")
        QMessageBox.warning(self, "下载失败", f"更新包下载失败：\n{error}")

    def _on_check_failed(self, error: str):
        """检查更新失败（静默处理，不打扰用户）"""
        self.status_label.setText("就绪 — 请选择一个文件夹开始")

    # ─────────── 关于对话框 ───────────

    def _show_about(self):
        QMessageBox.about(
            self,
            f"关于 — {__app_name__}",
            "<div style='color:#c9d1d9; line-height:1.8;'>"
            f"<h2 style='color:#58a6ff;'>⚡ {__app_name__}</h2>"
            f"<p>版本 {__version__} · PySide6 Demo</p>"
            "<hr style='border-color:#30363d;'>"
            "<p><b>功能特性：</b></p>"
            "<ul>"
            "<li>📁 添加前缀 / 后缀</li>"
            "<li>🔍 查找替换文本</li>"
            "<li>🔢 序号批量命名</li>"
            "<li>📝 修改扩展名</li>"
            "<li>↩️ 一键撤销</li>"
            "<li>🔄 开机自动检查更新</li>"
            "</ul>"
            "<p style='color:#8b949e;'>Python 3.12 + PySide6 6.11</p>"
            "</div>",
        )
