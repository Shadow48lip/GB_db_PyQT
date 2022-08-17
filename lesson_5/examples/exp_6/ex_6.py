"""Работа с БД через PyQt"""

import sys
from PyQt5 import QtWidgets, QtSql
from PyQt5.QtSql import QSqlQuery, QSqlDatabase

# Открытие базы данных SQLite
con1 = QtSql.QSqlDatabase.addDatabase('QSQLITE')
db_path_and_name = 'demo.sqlite'
con1.setDatabaseName(db_path_and_name)
print('is_DB_open :', con1.isOpen())
con1.open()
print('is_DB_open :', con1.isOpen())
print(con1.databaseName())
query = QSqlQuery()
# Добавляем нового артиста
query.exec("INSERT INTO Artist (Name) VALUES ('---The New Artist---')")
con1.close()
print('is_DB_open :', con1.isOpen())

"""
Смотрим результат в БД через DB Browser
"""

