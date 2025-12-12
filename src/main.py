"""
主程序入口
"""

import sys
from PyQt5.QtWidgets import QApplication
from src.main_window import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
