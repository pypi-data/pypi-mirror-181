import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QSizePolicy
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtCore import pyqtSlot, Qt


def window():
    app = QApplication(sys.argv)
    win = QWidget()
    sizePolicy = QSizePolicy()
    sizePolicy.setHeightForWidth(True)
    win.setSizePolicy(sizePolicy)
    grid = QGridLayout()
    size = 15

    for i in range(size):
        for j in range(size):
            cell_widget = QWidget()
            cell_widget.setAutoFillBackground(True)
            palette = cell_widget.palette()
            palette.setColor(cell_widget.backgroundRole(), QColor('red'))
            cell_widget.setPalette(palette)
            grid.addWidget(cell_widget, i, j)

    win.setLayout(grid)
    win.setWindowTitle("PyQt Grid Example")
    win.setGeometry(50, 50, 200, 200)
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    window()
