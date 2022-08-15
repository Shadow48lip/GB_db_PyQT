"""Обработчики событий, связанных с элементами интерфейса"""

import sys
from PyQt5 import QtWidgets


def on_clicked():
    print("Кнопка нажата. Функция on_clicked")


class MyClass:

    def __init__(self, x=0):
        self.x = x

    def __call__(self):
        print("Кнопка нажата. Метод MyClass.__call__()")
        print("x = ", self.x)

    def on_clicked(self):
        print("Кнопка нажата. Метод MyClass.on_clicked()")


obj = MyClass(5)
app = QtWidgets.QApplication(sys.argv)
button = QtWidgets.QPushButton("Нажми меня")

# В качестве обработчика назначается функция
button.clicked.connect(on_clicked)

# В качестве обработчика назначается результат выполнения функции
button.clicked.connect(lambda: on_clicked())

# В качестве обработчика назначается метод объекта
button.clicked.connect(obj.on_clicked)

# В качестве обработчика назначается экземпляр класса
button.clicked.connect(MyClass(10))

# В качестве обработчика назначается lambda-функция
button.clicked.connect(lambda: MyClass(5)())

button.show()
sys.exit(app.exec_())
