"""
批量文件重命名工具 — 入口文件
运行: python main.py
"""

import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QColor, QPalette

from app.main_window import MainWindow


def _apply_dark_palette(app: QApplication):
    """设置 Fusion 风格 + 深色调色板基底"""
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.Window,          QColor("#0d1117"))
    palette.setColor(QPalette.WindowText,      QColor("#c9d1d9"))
    palette.setColor(QPalette.Base,            QColor("#0d1117"))
    palette.setColor(QPalette.AlternateBase,   QColor("#161b22"))
    palette.setColor(QPalette.ToolTipBase,     QColor("#1c2128"))
    palette.setColor(QPalette.ToolTipText,     QColor("#c9d1d9"))
    palette.setColor(QPalette.Text,            QColor("#c9d1d9"))
    palette.setColor(QPalette.Button,          QColor("#21262d"))
    palette.setColor(QPalette.ButtonText,      QColor("#c9d1d9"))
    palette.setColor(QPalette.BrightText,      QColor("#f0f6fc"))
    palette.setColor(QPalette.Highlight,       QColor("#1f6feb"))
    palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))
    app.setPalette(palette)


def main():
    app = QApplication(sys.argv)
    _apply_dark_palette(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
