"""Работа с БД средствами Qt"""
# Использование модели, привязанной к таблице

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableView, QPushButton
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5 import QtCore


def add_record():
    """Вставляем пустую запись,
    в которую пользователь сможет ввести нужные данные"""
    MODEL.insertRow(MODEL.rowCount())


def del_record():
    """Удаляем запись из модели"""
    MODEL.removeRow(TV_OBJ.currentIndex().row())
    # Выполняем повторное считывание данных в модель,
    # чтобы убрать пустую "мусорную" запись
    MODEL.select()


APP = QApplication(sys.argv)

W_OBJ = QWidget()
W_OBJ.setWindowTitle("Модель-таблица")

# Устанавливаем соединение с базой данных
CONN = QSqlDatabase.addDatabase('QSQLITE')
CONN.setDatabaseName('test.sqlite3')
CONN.open()

# Создаем модель
MODEL = QSqlTableModel(parent=W_OBJ)
MODEL.setTable('vendors')
MODEL.setSort(1, QtCore.Qt.AscendingOrder)
MODEL.select()

# Задаем заголовки для столбцов модели
MODEL.setHeaderData(1, QtCore.Qt.Horizontal, 'Название')
MODEL.setHeaderData(2, QtCore.Qt.Horizontal, 'Телефон')
MODEL.setHeaderData(3, QtCore.Qt.Horizontal, 'Адрес')

# Создаём модель таблицы для формы и связываем её с данными
TV_OBJ = QTableView()
TV_OBJ.setModel(MODEL)

# Скрываем первый столбец, в котором выводится идентификатор
TV_OBJ.hideColumn(0)
TV_OBJ.setColumnWidth(1, 150)
TV_OBJ.setColumnWidth(2, 60)
TV_OBJ.setColumnWidth(3, 130)

# Задаем модель вертикального бокса для добавления кнопок
# https://doc.qt.io/qt-5/qvboxlayout.html
VBOX_OBJ = QVBoxLayout()
VBOX_OBJ.addWidget(TV_OBJ)

BTN_ADD = QPushButton("&Добавить запись")
BTN_ADD.clicked.connect(add_record)
VBOX_OBJ.addWidget(BTN_ADD)
BTN_DEL = QPushButton("&Удалить запись")
BTN_DEL.clicked.connect(del_record)
VBOX_OBJ.addWidget(BTN_DEL)

W_OBJ.setLayout(VBOX_OBJ)
W_OBJ.resize(400, 250)
W_OBJ.show()
sys.exit(APP.exec_())
