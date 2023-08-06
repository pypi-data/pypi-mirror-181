from PySide6.QtWidgets import QMainWindow, QApplication, QListWidget, QFileDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor
from malt.video_manager import VideoManager
import sys

from malt.py_ui.ui_core_window import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.listWidget = QListWidget()
        self.video_manager = VideoManager(self)
        self.ui.scrollArea.setWidget(self.listWidget)

    def keyPressEvent(self, event):
        self.video_manager.pass_keypress(event)


def main():
    app = QApplication()
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


# if __name__ == "__main__":
#     main()
