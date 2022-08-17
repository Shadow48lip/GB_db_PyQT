"""Связка слайдера и прогресс-бара"""

import sys
from PyQt5.QtWidgets import QDialog, QWidget, QApplication
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
import slider
import progress


class SliderClass(QDialog):
    # Добавляем Qt-сигнал как атрибут класса
    changed_value = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.sd = slider.Ui_SliderDialog()
        self.sd.setupUi(self)

        # Связываем оригинальный сигнал слайдера с функцией данного класса
        # при передвигании слайдер будет срабатывать ф-ция on_changed_value
        self.sd.horizontalSlider.valueChanged.connect(self.on_changed_value)

    def on_changed_value(self, value):
        # В этой ф-ции on_changed_value мы генерируем сигнал
        self.changed_value.emit(value)


class ProgressClass(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = progress.Ui_ProgressDialog()
        self.ui.setupUi(self)

    def make_connection(self, slider_object):
        # Связываем "свой" сигнал со "своим" слотом
        slider_object.changed_value.connect(self.get_slider_value)

    # Создаем Qt-слот
    @pyqtSlot(int)
    def get_slider_value(self, val):
        self.ui.progressBar.setValue(val)


if __name__ == '__main__':
    APP = QApplication(sys.argv)
    SLIDER = SliderClass()
    PROGRESS = ProgressClass()
    # Непосредственное связывание ProgressBar'а и Sliser'а
    PROGRESS.make_connection(SLIDER)
    # отображаем слайдер
    SLIDER.show()
    # отображаем прогресс-бар
    PROGRESS.show()
    sys.exit(APP.exec_())
