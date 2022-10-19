from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow, QWidget, QApplication
from PyQt6 import uic
import sys

app = QApplication(sys.argv)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scr = uic.loadUi("main_scr.ui")
        


window = MainWindow()
window.scr.show()
app.exec()
sys.exit(app)