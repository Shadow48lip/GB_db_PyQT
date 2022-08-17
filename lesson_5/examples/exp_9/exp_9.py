"""Модель, поддерживающая межтабличные связи"""
# Использование модели QSqlRelationalTableModel

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableView, QPushButton
from PyQt5.QtSql import QSqlDatabase, QSqlRelationalTableModel, QSqlRelation, QSqlTableModel, QSqlRelationalDelegate
from PyQt5 import QtCore


def add_record():
    """Добавить запись"""
    R_T_MODEL.insertRow(R_T_MODEL.rowCount())


def del_record():
    """Удалить запись"""
    R_T_MODEL.removeRow(TV_OBJ.currentIndex().row())
    R_T_MODEL.select()


# объект приложения
APP = QApplication(sys.argv)

# виджет-окно
W_OBJ = QWidget()
W_OBJ.setWindowTitle("Связь с внешней таблицей")

# соединяемся с БД
CONN = QSqlDatabase.addDatabase('QSQLITE')
CONN.setDatabaseName('test.sqlite3')
CONN.open()

# модель-связанная таблица
R_T_MODEL = QSqlRelationalTableModel(parent=W_OBJ)
R_T_MODEL.setEditStrategy(QSqlTableModel.OnManualSubmit)
R_T_MODEL.setTable('product')
R_T_MODEL.setSort(1, QtCore.Qt.AscendingOrder)

# Задаем для поля категории связь с таблицей списка категорий
R_T_MODEL.setRelation(1, QSqlRelation('category', 'id', 'name'))
# 'category', 'id', 'category' (имя первичной таблицы,
# имя поля первичного ключа, имя поля, выводящегося на экран)
R_T_MODEL.select()
R_T_MODEL.setHeaderData(1, QtCore.Qt.Horizontal, 'Категория товара')
R_T_MODEL.setHeaderData(2, QtCore.Qt.Horizontal, 'Название товара')
R_T_MODEL.dataChanged.connect(R_T_MODEL.submitAll)

# Размещаем объекты
VBOX_OBJ = QVBoxLayout()
TV_OBJ = QTableView()
TV_OBJ.setModel(R_T_MODEL)
TV_OBJ.setItemDelegateForColumn(1, QSqlRelationalDelegate(TV_OBJ))
TV_OBJ.hideColumn(0)
TV_OBJ.setColumnWidth(1, 150)
TV_OBJ.setColumnWidth(2, 150)
VBOX_OBJ.addWidget(TV_OBJ)

# Добавляем кнопки
BTN_ADD = QPushButton("&Добавить запись")
BTN_ADD.clicked.connect(add_record)
VBOX_OBJ.addWidget(BTN_ADD)
BTN_DEL = QPushButton("&Удалить запись")
BTN_DEL.clicked.connect(del_record)
VBOX_OBJ.addWidget(BTN_DEL)

# Формируем итоговое окно
W_OBJ.setLayout(VBOX_OBJ)
W_OBJ.resize(430, 250)
W_OBJ.show()

sys.exit(APP.exec_())
