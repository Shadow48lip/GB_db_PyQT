# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'slider.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SliderDialog(object):
    def setupUi(self, SliderDialog):
        SliderDialog.setObjectName("SliderDialog")
        SliderDialog.resize(240, 45)

        self.horizontalSlider = QtWidgets.QSlider(SliderDialog)
        self.horizontalSlider.setGeometry(QtCore.QRect(20, 10, 160, 19))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")

        self.retranslateUi(SliderDialog)
        QtCore.QMetaObject.connectSlotsByName(SliderDialog)

    def retranslateUi(self, SliderDialog):
        _translate = QtCore.QCoreApplication.translate
        SliderDialog.setWindowTitle(_translate("SliderDialog", "Slider"))

