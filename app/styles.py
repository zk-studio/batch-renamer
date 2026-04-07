"""
QSS 样式表 — 现代深色主题
所有 UI 样式集中在此管理，方便统一调整。
"""

# ── 调色板常量 ──
COLORS = {
    "bg_primary":    "#0d1117",   # 最深背景
    "bg_secondary":  "#161b22",   # 次级背景
    "bg_tertiary":   "#1c2128",   # 弹出层背景
    "bg_card":       "#21262d",   # 卡片 / 按钮背景
    "border":        "#30363d",   # 边框
    "border_active": "#58a6ff",   # 激活态边框
    "text_primary":  "#c9d1d9",   # 主文字
    "text_secondary":"#8b949e",   # 次级文字
    "text_muted":    "#484f58",   # 弱文字
    "text_bright":   "#f0f6fc",   # 强调文字
    "accent_blue":   "#1f6feb",   # 蓝色强调
    "accent_blue_l": "#58a6ff",   # 浅蓝
    "accent_blue_m": "#388bfd",   # 中蓝
    "accent_green":  "#238636",   # 绿色
    "accent_green_l":"#3fb950",   # 浅绿
    "accent_green_m":"#2ea043",   # 中绿
    "accent_red":    "#da3633",   # 红色
    "accent_red_l":  "#f85149",   # 浅红
    "highlight":     "#1f6feb33", # 选中高亮（半透明）
}


STYLESHEET = """
/* ═══════════════════════════════════════════
   全局基础
   ═══════════════════════════════════════════ */
* {
    font-family: "Segoe UI", "Microsoft YaHei UI", sans-serif;
    font-size: 13px;
}

QMainWindow {
    background-color: #0d1117;
}

/* ═══════════════════════════════════════════
   菜单栏
   ═══════════════════════════════════════════ */
QMenuBar {
    background-color: #161b22;
    color: #c9d1d9;
    border-bottom: 1px solid #21262d;
    padding: 2px 0;
}
QMenuBar::item {
    padding: 6px 14px;
    border-radius: 6px;
    margin: 2px 2px;
}
QMenuBar::item:selected {
    background-color: #1f6feb33;
    color: #58a6ff;
}

QMenu {
    background-color: #1c2128;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 6px;
}
QMenu::item {
    padding: 8px 28px 8px 16px;
    border-radius: 6px;
    color: #c9d1d9;
}
QMenu::item:selected {
    background-color: #1f6feb44;
    color: #58a6ff;
}
QMenu::separator {
    height: 1px;
    background: #30363d;
    margin: 4px 10px;
}

/* ═══════════════════════════════════════════
   分组框 (GroupBox)
   ═══════════════════════════════════════════ */
QGroupBox {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    margin-top: 18px;
    padding: 20px 16px 12px 16px;
    color: #c9d1d9;
    font-weight: bold;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 20px;
    padding: 0 10px;
    color: #58a6ff;
    font-size: 13px;
}

/* ═══════════════════════════════════════════
   按钮
   ═══════════════════════════════════════════ */
QPushButton {
    background-color: #21262d;
    color: #c9d1d9;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: 600;
    min-height: 18px;
}
QPushButton:hover {
    background-color: #30363d;
    border-color: #58a6ff;
    color: #ffffff;
}
QPushButton:pressed {
    background-color: #1f6feb;
    border-color: #1f6feb;
}
QPushButton:disabled {
    background-color: #161b22;
    color: #484f58;
    border-color: #21262d;
}

/* ── 主操作按钮（绿色渐变） ── */
QPushButton#btnRename {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #238636, stop:1 #2ea043);
    color: #ffffff;
    border: none;
    font-size: 14px;
    padding: 10px 32px;
    border-radius: 10px;
}
QPushButton#btnRename:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #2ea043, stop:1 #3fb950);
}
QPushButton#btnRename:pressed {
    background-color: #238636;
}
QPushButton#btnRename:disabled {
    background-color: #21262d;
    color: #484f58;
}

/* ── 文件夹选择按钮（蓝色渐变） ── */
QPushButton#btnSelectFolder {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #1f6feb, stop:1 #388bfd);
    color: #ffffff;
    border: none;
    padding: 10px 24px;
    border-radius: 10px;
}
QPushButton#btnSelectFolder:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #388bfd, stop:1 #58a6ff);
}

/* ── 撤销按钮（红色渐变） ── */
QPushButton#btnUndo {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #da3633, stop:1 #f85149);
    color: #ffffff;
    border: none;
    border-radius: 10px;
    padding: 10px 24px;
}
QPushButton#btnUndo:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #f85149, stop:1 #ff7b72);
}
QPushButton#btnUndo:disabled {
    background-color: #21262d;
    color: #484f58;
}

/* ═══════════════════════════════════════════
   输入框
   ═══════════════════════════════════════════ */
QLineEdit {
    background-color: #0d1117;
    color: #c9d1d9;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 8px 12px;
    selection-background-color: #1f6feb;
}
QLineEdit:focus {
    border-color: #58a6ff;
    background-color: #161b22;
}
QLineEdit:disabled {
    background-color: #0d1117;
    color: #484f58;
}

/* ═══════════════════════════════════════════
   下拉框
   ═══════════════════════════════════════════ */
QComboBox {
    background-color: #0d1117;
    color: #c9d1d9;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 8px 12px;
    min-width: 120px;
}
QComboBox:hover {
    border-color: #58a6ff;
}
QComboBox::drop-down {
    border: none;
    width: 30px;
}
QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #58a6ff;
    margin-right: 10px;
}
QComboBox QAbstractItemView {
    background-color: #1c2128;
    border: 1px solid #30363d;
    border-radius: 8px;
    color: #c9d1d9;
    selection-background-color: #1f6feb44;
    selection-color: #58a6ff;
    padding: 4px;
    outline: none;
}

/* ═══════════════════════════════════════════
   数字输入框
   ═══════════════════════════════════════════ */
QSpinBox {
    background-color: #0d1117;
    color: #c9d1d9;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 6px 10px;
}
QSpinBox:focus {
    border-color: #58a6ff;
}
QSpinBox::up-button, QSpinBox::down-button {
    background-color: #21262d;
    border: none;
    width: 20px;
    border-radius: 4px;
}
QSpinBox::up-button:hover, QSpinBox::down-button:hover {
    background-color: #30363d;
}

/* ═══════════════════════════════════════════
   复选框
   ═══════════════════════════════════════════ */
QCheckBox {
    color: #c9d1d9;
    spacing: 8px;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 1px solid #30363d;
    background-color: #0d1117;
}
QCheckBox::indicator:checked {
    background-color: #1f6feb;
    border-color: #1f6feb;
}
QCheckBox::indicator:hover {
    border-color: #58a6ff;
}

/* ═══════════════════════════════════════════
   表格 (TableWidget)
   ═══════════════════════════════════════════ */
QTableWidget {
    background-color: #0d1117;
    color: #c9d1d9;
    border: 1px solid #30363d;
    border-radius: 10px;
    gridline-color: #21262d;
    selection-background-color: #1f6feb33;
    selection-color: #58a6ff;
    outline: none;
}
QTableWidget::item {
    padding: 6px 10px;
    border-bottom: 1px solid #161b22;
}
QTableWidget::item:selected {
    background-color: #1f6feb22;
    color: #58a6ff;
}

QHeaderView::section {
    background-color: #161b22;
    color: #8b949e;
    border: none;
    border-bottom: 2px solid #21262d;
    border-right: 1px solid #21262d;
    padding: 10px 12px;
    font-weight: bold;
    font-size: 12px;
    text-transform: uppercase;
}
QHeaderView::section:first {
    border-top-left-radius: 10px;
}
QHeaderView::section:last {
    border-top-right-radius: 10px;
    border-right: none;
}

/* ═══════════════════════════════════════════
   滚动条
   ═══════════════════════════════════════════ */
QScrollBar:vertical {
    background: #0d1117;
    width: 10px;
    margin: 0;
    border-radius: 5px;
}
QScrollBar::handle:vertical {
    background: #30363d;
    border-radius: 5px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background: #484f58;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
QScrollBar:horizontal {
    background: #0d1117;
    height: 10px;
    border-radius: 5px;
}
QScrollBar::handle:horizontal {
    background: #30363d;
    border-radius: 5px;
    min-width: 30px;
}
QScrollBar::handle:horizontal:hover {
    background: #484f58;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0;
}

/* ═══════════════════════════════════════════
   状态栏
   ═══════════════════════════════════════════ */
QStatusBar {
    background-color: #161b22;
    color: #8b949e;
    border-top: 1px solid #21262d;
    padding: 4px 12px;
    font-size: 12px;
}
QStatusBar QLabel {
    color: #8b949e;
}

/* ═══════════════════════════════════════════
   进度条
   ═══════════════════════════════════════════ */
QProgressBar {
    background-color: #21262d;
    border: none;
    border-radius: 6px;
    text-align: center;
    color: #c9d1d9;
    font-size: 11px;
    max-height: 14px;
}
QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #1f6feb, stop:1 #58a6ff);
    border-radius: 6px;
}

/* ═══════════════════════════════════════════
   自定义 ObjectName 标签
   ═══════════════════════════════════════════ */
QLabel#labelHint {
    color: #484f58;
    font-size: 12px;
}
QLabel#labelPath {
    color: #58a6ff;
    font-size: 13px;
}
QLabel#labelTitle {
    color: #f0f6fc;
    font-size: 20px;
    font-weight: bold;
}
QLabel#labelSubtitle {
    color: #8b949e;
    font-size: 12px;
}
QLabel#labelStats {
    color: #3fb950;
    font-size: 13px;
    font-weight: 600;
}
"""
