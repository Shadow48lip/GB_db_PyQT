# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'search_form.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FinderForm(object):
    def setupUi(self, FinderForm):
        FinderForm.setObjectName("FinderForm")
        FinderForm.resize(634, 482)
        self.pushButton = QtWidgets.QPushButton(FinderForm)
        self.pushButton.setGeometry(QtCore.QRect(10, 220, 111, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(FinderForm)
        self.pushButton_2.setEnabled(False)
        self.pushButton_2.setGeometry(QtCore.QRect(130, 220, 111, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit = QtWidgets.QLineEdit(FinderForm)
        self.lineEdit.setGeometry(QtCore.QRect(10, 30, 611, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(FinderForm)
        self.label.setGeometry(QtCore.QRect(10, 10, 111, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(FinderForm)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 281, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(FinderForm)
        self.label_3.setGeometry(QtCore.QRect(10, 280, 281, 16))
        self.label_3.setObjectName("label_3")
        self.progressBar = QtWidgets.QProgressBar(FinderForm)
        self.progressBar.setGeometry(QtCore.QRect(10, 250, 611, 16))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(FinderForm)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 300, 611, 171))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(FinderForm)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(10, 80, 611, 131))
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")

        self.retranslateUi(FinderForm)
        QtCore.QMetaObject.connectSlotsByName(FinderForm)

    def retranslateUi(self, FinderForm):
        _translate = QtCore.QCoreApplication.translate
        FinderForm.setWindowTitle(_translate("FinderForm", "Поисковик"))
        self.pushButton.setText(_translate("FinderForm", "Запустить поиск"))
        self.pushButton_2.setText(_translate("FinderForm", "Остановить поиск"))
        self.lineEdit.setText(_translate("FinderForm", "python"))
        self.label.setText(_translate("FinderForm", "Текст для поиска"))
        self.label_2.setText(_translate("FinderForm", "Список URL для просмотра (один URL на строке)"))
        self.label_3.setText(_translate("FinderForm", "Результаты поиска"))
        self.plainTextEdit_2.setPlainText(_translate("FinderForm", "http://www.python.org/\n"
"https://habrahabr.ru/search/?q=%5Bpython%5D\n"
"https://python-scripts.com/"))

