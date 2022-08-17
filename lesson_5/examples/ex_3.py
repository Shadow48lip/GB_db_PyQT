"""Перехват параметров событий"""

import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication


class WindowClass(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.resize(300, 100)

    def event(self, e):
        if e.type() == QtCore.QEvent.KeyPress:
            print("Вы нажали клавишу на клавиатуре")
            print(f'Код: {e.key()}, текст: {e.text()}')
        elif e.type() == QtCore.QEvent.Close:
            print("Вы закрыли окно")
        elif e.type() == QtCore.QEvent.MouseButtonPress:
            print(f'Совершен клик мышью. Координаты: {e.x()}, {e.y()}')

        # Событие отправляется дальше
        return super().event(e)


if __name__ == '__main__':
    APP = QApplication(sys.argv)
    WC_OBJ = WindowClass()
    WC_OBJ.show()
    sys.exit(APP.exec_())
