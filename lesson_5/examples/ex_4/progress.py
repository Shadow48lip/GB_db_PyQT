# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'progress.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ProgressDialog(object):
    def setupUi(self, ProgressDialog):
        ProgressDialog.setObjectName("ProgressDialog")
        ProgressDialog.resize(237, 44)
        self.progressBar = QtWidgets.QProgressBar(ProgressDialog)
        self.progressBar.setGeometry(QtCore.QRect(10, 10, 211, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")

        self.retranslateUi(ProgressDialog)
        QtCore.QMetaObject.connectSlotsByName(ProgressDialog)

    def retranslateUi(self, ProgressDialog):
        _translate = QtCore.QCoreApplication.translate
        ProgressDialog.setWindowTitle(_translate("ProgressDialog", "Progress"))

