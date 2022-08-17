"""Работа с БД средствами Qt"""
# Использование модели, привязанной к SQL-запросу

import sys
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5 import QtCore

APP = QApplication(sys.argv)

T_WIND = QTableView()
T_WIND.setWindowTitle("Виджет-таблица на основе модели-запроса")

# Устанавливаем соединение с базой данных
CONN = QSqlDatabase.addDatabase('QSQLITE')
# Определяем путь до базы данных
CONN.setDatabaseName('test.sqlite3')
# Открываем базу данных
CONN.open()

# Создаем модель
T_QUERY = QSqlQueryModel()
T_QUERY.setQuery("SELECT * FROM vendors ORDER BY name")
# Задаем заголовки для столбцов модели
T_QUERY.setHeaderData(1, QtCore.Qt.Horizontal, 'Название')
T_QUERY.setHeaderData(2, QtCore.Qt.Horizontal, 'Телефон')
T_QUERY.setHeaderData(3, QtCore.Qt.Horizontal, 'Адрес')

# Задаем для таблицы только что созданную модель
T_WIND.setModel(T_QUERY)
# Скрываем первый столбец, в котором выводится идентификатор
T_WIND.hideColumn(0)
T_WIND.setColumnWidth(1, 150)
T_WIND.setColumnWidth(2, 100)
T_WIND.setColumnWidth(3, 200)
T_WIND.resize(470, 130)

T_WIND.show()
sys.exit(APP.exec_())
