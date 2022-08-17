"""
Подключаем файл с разметкой интерфейса, созданного через qtdesigner
(вариант без создания класса MyWindow)
"""

import sys
from PyQt5.QtWidgets import QWidget, QApplication, qApp
from PyQt5 import uic


app = QApplication(sys.argv)
window_obj = QWidget()
UI = uic.loadUi('test.ui', window_obj)
UI.btnQuit.clicked.connect(qApp.quit)
window_obj.show()

sys.exit(app.exec_())
