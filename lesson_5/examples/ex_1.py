"""Создание и генерация собственного сигнала"""

import sys
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow, QApplication


# Базовый класс для всех объектов модуля
class AnyObject(QObject):
    # Создаем свой сигнал
    own_signal = pyqtSignal()


# Создаем главное окно
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.set_params()

    def set_params(self):
        """Устанавливаем параметры"""
        self.obj = AnyObject()
        # Обработчик сигнала, связанного с объектом
        self.obj.own_signal.connect(self.close)
        # Параметры главного окна
        self.setGeometry(900, 300, 290, 150)
        self.setWindowTitle('Emit signal')
        self.show()

    # Метод, который срабатывает при нажатии на окно
    def mousePressEvent(self, event):
        """
        Генерируем сигнал
        """
        self.obj.own_signal.emit()


if __name__ == '__main__':
    APP = QApplication(sys.argv)
    MW_OBJ = MainWindow()
    sys.exit(APP.exec_())
