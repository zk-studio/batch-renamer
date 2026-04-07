"""
自定义控件组件
可复用的 UI 小部件，保持主窗口代码简洁。
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QLineEdit, QComboBox,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QGroupBox, QCheckBox, QSpinBox, QFileDialog,
    QAbstractItemView,
)

from .rename_engine import RenameMode, RenameParams


class FolderSelector(QGroupBox):
    """
    文件夹选择控件：路径显示 + 选择按钮
    发射 folderSelected(str) 信号
    """
    folderSelected = Signal(str)

    def __init__(self, parent=None):
        super().__init__("📂 目标文件夹", parent)
        layout = QHBoxLayout(self)
        layout.setSpacing(10)

        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("点击右侧按钮选择文件夹 …")
        self.path_edit.setReadOnly(True)
        self.path_edit.setObjectName("labelPath")

        self.btn_select = QPushButton("📁  选择文件夹")
        self.btn_select.setObjectName("btnSelectFolder")
        self.btn_select.setCursor(Qt.PointingHandCursor)
        self.btn_select.clicked.connect(self._on_click)

        layout.addWidget(self.path_edit, 1)
        layout.addWidget(self.btn_select)

    def _on_click(self):
        folder = QFileDialog.getExistingDirectory(
            self, "选择目标文件夹", "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
        )
        if folder:
            self.path_edit.setText(folder)
            self.folderSelected.emit(folder)

    def set_path(self, path: str):
        self.path_edit.setText(path)

    def clear(self):
        self.path_edit.clear()


class RulePanel(QGroupBox):
    """
    重命名规则面板：模式选择 + 参数输入 + 筛选
    发射 paramsChanged() 信号
    """
    paramsChanged = Signal()

    def __init__(self, parent=None):
        super().__init__("🛠️ 重命名规则", parent)
        grid = QGridLayout(self)
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(12)

        # ── 模式选择 ──
        grid.addWidget(QLabel("模式："), 0, 0)
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([m.label for m in RenameMode])
        self.mode_combo.currentIndexChanged.connect(self._on_mode_change)
        grid.addWidget(self.mode_combo, 0, 1, 1, 2)

        # ── 输入 1 ──
        self.lbl_input1 = QLabel("前缀文本：")
        grid.addWidget(self.lbl_input1, 1, 0)
        self.input1 = QLineEdit()
        self.input1.setPlaceholderText("例: IMG_")
        self.input1.textChanged.connect(self._emit_changed)
        grid.addWidget(self.input1, 1, 1, 1, 2)

        # ── 输入 2（查找替换） ──
        self.lbl_input2 = QLabel("替换为：")
        grid.addWidget(self.lbl_input2, 2, 0)
        self.input2 = QLineEdit()
        self.input2.setPlaceholderText("例: photo_")
        self.input2.textChanged.connect(self._emit_changed)
        grid.addWidget(self.input2, 2, 1, 1, 2)

        # ── 序号起始 ──
        self.lbl_start = QLabel("起始编号：")
        grid.addWidget(self.lbl_start, 3, 0)
        self.spin_start = QSpinBox()
        self.spin_start.setRange(0, 99999)
        self.spin_start.setValue(1)
        self.spin_start.valueChanged.connect(self._emit_changed)
        grid.addWidget(self.spin_start, 3, 1)

        # ── 编号位数 ──
        self.lbl_digits = QLabel("编号位数：")
        grid.addWidget(self.lbl_digits, 3, 2)
        self.spin_digits = QSpinBox()
        self.spin_digits.setRange(1, 10)
        self.spin_digits.setValue(3)
        self.spin_digits.valueChanged.connect(self._emit_changed)
        grid.addWidget(self.spin_digits, 3, 3)

        # ── 文件筛选 ──
        grid.addWidget(QLabel("文件筛选："), 4, 0)
        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText("例: .jpg .png（留空 = 全部文件）")
        grid.addWidget(self.filter_edit, 4, 1, 1, 2)

        self.chk_subdirs = QCheckBox("包含子文件夹中的文件")
        grid.addWidget(self.chk_subdirs, 4, 3)

        # 初始化可见性
        self._on_mode_change(0)

    # ── 信号转发 ──
    def _emit_changed(self):
        self.paramsChanged.emit()

    # ── 模式切换 ──
    def _on_mode_change(self, index: int):
        # 隐藏所有可选项
        for w in (self.lbl_input2, self.input2,
                  self.lbl_start, self.spin_start,
                  self.lbl_digits, self.spin_digits):
            w.setVisible(False)

        self.input1.setVisible(True)
        self.lbl_input1.setVisible(True)

        mode = RenameMode(index)

        if mode == RenameMode.ADD_PREFIX:
            self.lbl_input1.setText("前缀文本：")
            self.input1.setPlaceholderText("例: IMG_")
        elif mode == RenameMode.ADD_SUFFIX:
            self.lbl_input1.setText("后缀文本：")
            self.input1.setPlaceholderText("例: _backup")
        elif mode == RenameMode.FIND_REPLACE:
            self.lbl_input1.setText("查找：")
            self.input1.setPlaceholderText("要查找的文本")
            self.lbl_input2.setVisible(True)
            self.input2.setVisible(True)
            self.input2.setPlaceholderText("替换成的文本")
        elif mode == RenameMode.SEQUENTIAL:
            self.lbl_input1.setText("文件名模板：")
            self.input1.setPlaceholderText("例: photo（编号会自动追加）")
            self.lbl_start.setVisible(True)
            self.spin_start.setVisible(True)
            self.lbl_digits.setVisible(True)
            self.spin_digits.setVisible(True)
        elif mode == RenameMode.CHANGE_EXT:
            self.lbl_input1.setText("新扩展名：")
            self.input1.setPlaceholderText("例: .txt")

        self._emit_changed()

    # ── 获取当前参数 ──
    def get_params(self) -> RenameParams:
        return RenameParams(
            mode=RenameMode(self.mode_combo.currentIndex()),
            text1=self.input1.text(),
            text2=self.input2.text(),
            seq_start=self.spin_start.value(),
            seq_digits=self.spin_digits.value(),
        )

    def get_ext_filter(self) -> str:
        return self.filter_edit.text().strip()

    def get_include_subdirs(self) -> bool:
        return self.chk_subdirs.isChecked()


class PreviewTable(QGroupBox):
    """
    文件预览表格：显示原文件名 → 新文件名对照
    带空状态提示
    """

    def __init__(self, parent=None):
        super().__init__("👀 预览", parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 12, 8, 8)

        # 空状态占位符
        self.empty_label = QLabel("📭  尚未加载文件\n请先选择一个文件夹")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet(
            "color: #484f58; font-size: 16px; padding: 40px;"
        )
        layout.addWidget(self.empty_label)

        # 表格
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["序号", "原文件名", "新文件名"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.setVisible(False)

        layout.addWidget(self.table)

    def update_preview(self, preview_data: list[tuple[str, str, bool]]):
        """
        刷新表格显示。

        Args:
            preview_data: [(原名, 新名, 是否有变化), ...]
        """
        if not preview_data:
            self.table.setRowCount(0)
            self.table.setVisible(False)
            self.empty_label.setVisible(True)
            return

        self.empty_label.setVisible(False)
        self.table.setVisible(True)
        self.table.setRowCount(len(preview_data))

        for i, (original, new_name, changed) in enumerate(preview_data):
            # 序号
            idx_item = QTableWidgetItem(str(i + 1))
            idx_item.setTextAlignment(Qt.AlignCenter)
            idx_item.setForeground(QColor("#8b949e"))
            self.table.setItem(i, 0, idx_item)

            # 原文件名
            orig_item = QTableWidgetItem(original)
            orig_item.setForeground(QColor("#c9d1d9"))
            self.table.setItem(i, 1, orig_item)

            # 新文件名
            new_item = QTableWidgetItem(new_name)
            if changed:
                new_item.setForeground(QColor("#3fb950"))
            else:
                new_item.setForeground(QColor("#484f58"))
            self.table.setItem(i, 2, new_item)

    @property
    def has_data(self) -> bool:
        return self.table.rowCount() > 0

    def clear(self):
        self.table.setRowCount(0)
        self.table.setVisible(False)
        self.empty_label.setVisible(True)
