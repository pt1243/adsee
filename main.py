import sys

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(0, 0, 1280, 720)
        self.setWindowTitle('Link Budget Calculator')
        self.init_ui()

    def init_ui(self):
        self.label = QLabel(self)
        self.label.setText('Test label')
        self.label.move(100, 100)

        self.b1 = QPushButton(self)
        self.b1.setText('Click here')
        self.b1.clicked.connect(self.clicked)

    def clicked(self):
        self.label.setText('You pressed the button')
        self.update()

    def update(self):
        self.label.adjustSize()


def window():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


window()
