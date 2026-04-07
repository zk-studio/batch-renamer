"""
重命名核心引擎 — 与 UI 完全解耦
负责：文件扫描、名称计算、执行重命名、撤销
"""

import os
from dataclasses import dataclass, field
from enum import IntEnum, auto
from typing import Optional


# ── 重命名模式枚举 ──
class RenameMode(IntEnum):
    ADD_PREFIX   = 0   # 添加前缀
    ADD_SUFFIX   = 1   # 添加后缀
    FIND_REPLACE = 2   # 查找替换
    SEQUENTIAL   = 3   # 序号命名
    CHANGE_EXT   = 4   # 修改扩展名

    @property
    def label(self) -> str:
        return _MODE_LABELS[self]

_MODE_LABELS = {
    RenameMode.ADD_PREFIX:   "添加前缀",
    RenameMode.ADD_SUFFIX:   "添加后缀",
    RenameMode.FIND_REPLACE: "查找替换",
    RenameMode.SEQUENTIAL:   "序号命名",
    RenameMode.CHANGE_EXT:   "扩展名修改",
}


# ── 重命名参数 ──
@dataclass
class RenameParams:
    """重命名操作的所有参数"""
    mode: RenameMode = RenameMode.ADD_PREFIX
    text1: str = ""           # 前缀 / 后缀 / 查找文本 / 模板名 / 新扩展名
    text2: str = ""           # 替换文本（仅查找替换模式）
    seq_start: int = 1        # 序号起始值
    seq_digits: int = 3       # 序号位数


# ── 操作结果 ──
@dataclass
class RenameResult:
    """一次批量重命名的结果"""
    success_count: int = 0
    errors: list[str] = field(default_factory=list)
    history: list[tuple[str, str]] = field(default_factory=list)  # (new_path, old_path)


class RenameEngine:
    """
    重命名引擎：管理文件扫描、名称计算和重命名执行。
    所有路径操作都在这里完成，UI 层只需调用方法即可。
    """

    def __init__(self):
        self._undo_stack: list[list[tuple[str, str]]] = []

    # ── 扫描文件 ──
    @staticmethod
    def scan_files(
        folder: str,
        ext_filter: str = "",
        include_subdirs: bool = False,
    ) -> list[str]:
        """
        扫描目标文件夹，返回相对路径文件列表。

        Args:
            folder: 目标文件夹绝对路径
            ext_filter: 扩展名筛选（如 ".jpg .png"），空字符串不筛选
            include_subdirs: 是否递归扫描子文件夹

        Returns:
            排序后的文件相对路径列表
        """
        if not folder or not os.path.isdir(folder):
            return []

        # 解析扩展名筛选
        ext_set: set[str] = set()
        if ext_filter.strip():
            for part in ext_filter.replace(",", " ").split():
                ext = part.strip()
                if ext and not ext.startswith("."):
                    ext = "." + ext
                if ext:
                    ext_set.add(ext.lower())

        files: list[str] = []

        if include_subdirs:
            for root, _, filenames in os.walk(folder):
                for f in sorted(filenames):
                    if ext_set:
                        _, ext = os.path.splitext(f)
                        if ext.lower() not in ext_set:
                            continue
                    rel = os.path.relpath(os.path.join(root, f), folder)
                    files.append(rel)
        else:
            for f in sorted(os.listdir(folder)):
                full = os.path.join(folder, f)
                if os.path.isfile(full):
                    if ext_set:
                        _, ext = os.path.splitext(f)
                        if ext.lower() not in ext_set:
                            continue
                    files.append(f)

        return files

    # ── 计算新文件名 ──
    @staticmethod
    def compute_new_name(original: str, index: int, params: RenameParams) -> str:
        """
        根据重命名参数计算单个文件的新名称。

        Args:
            original: 原始文件名（可包含相对子路径）
            index: 文件在列表中的序号（从 0 开始）
            params: 重命名参数

        Returns:
            计算后的新文件名
        """
        basename = os.path.basename(original)
        name, ext = os.path.splitext(basename)
        dir_part = os.path.dirname(original)

        mode = params.mode

        if mode == RenameMode.ADD_PREFIX:
            new_base = params.text1 + name + ext

        elif mode == RenameMode.ADD_SUFFIX:
            new_base = name + params.text1 + ext

        elif mode == RenameMode.FIND_REPLACE:
            if params.text1:
                new_name = name.replace(params.text1, params.text2)
                new_ext = ext.replace(params.text1, params.text2) if params.text1 in ext else ext
                new_base = new_name + new_ext
            else:
                new_base = name + ext

        elif mode == RenameMode.SEQUENTIAL:
            template = params.text1 or "file"
            num = str(params.seq_start + index).zfill(params.seq_digits)
            new_base = f"{template}_{num}{ext}"

        elif mode == RenameMode.CHANGE_EXT:
            new_ext = params.text1.strip()
            if new_ext and not new_ext.startswith("."):
                new_ext = "." + new_ext
            new_base = name + (new_ext if new_ext else ext)

        else:
            new_base = name + ext

        return os.path.join(dir_part, new_base) if dir_part else new_base

    # ── 批量计算预览 ──
    @staticmethod
    def compute_preview(
        file_list: list[str],
        params: RenameParams,
    ) -> list[tuple[str, str, bool]]:
        """
        批量计算所有文件的新名称，返回预览列表。

        Returns:
            [(原名, 新名, 是否有变化), ...]
        """
        results = []
        for i, original in enumerate(file_list):
            new_name = RenameEngine.compute_new_name(original, i, params)
            changed = (new_name != original)
            results.append((original, new_name, changed))
        return results

    # ── 执行重命名 ──
    def execute(self, folder: str, file_list: list[str], params: RenameParams) -> RenameResult:
        """
        执行批量重命名。

        Args:
            folder: 目标文件夹绝对路径
            file_list: 文件相对路径列表
            params: 重命名参数

        Returns:
            RenameResult 包含成功数、错误列表和历史记录
        """
        result = RenameResult()

        for i, original in enumerate(file_list):
            new_name = self.compute_new_name(original, i, params)
            if new_name == original:
                continue

            old_path = os.path.join(folder, original)
            new_path = os.path.join(folder, new_name)

            try:
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
                os.rename(old_path, new_path)
                result.history.append((new_path, old_path))
                result.success_count += 1
            except Exception as e:
                result.errors.append(f"{original}: {e}")

        # 入栈用于撤销
        if result.history:
            self._undo_stack.append(result.history)

        return result

    # ── 撤销 ──
    def undo(self) -> RenameResult:
        """
        撤销最近一次重命名操作。

        Returns:
            RenameResult 成功/失败信息
        """
        result = RenameResult()

        if not self._undo_stack:
            return result

        last_batch = self._undo_stack.pop()
        for new_path, old_path in reversed(last_batch):
            try:
                os.rename(new_path, old_path)
                result.success_count += 1
            except Exception as e:
                result.errors.append(f"{os.path.basename(new_path)}: {e}")

        return result

    @property
    def can_undo(self) -> bool:
        return len(self._undo_stack) > 0

    @property
    def undo_depth(self) -> int:
        return len(self._undo_stack)
