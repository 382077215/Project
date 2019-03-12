# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test6.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Wait2(object):
    def __init__(self,Form):
        self.setupUi(Form)
        self.out(None)
    def setupUi(self, Form):
        self.yes_2 = QtWidgets.QPushButton(Form)
        self.yes_2.setGeometry(QtCore.QRect(260, 310, 171, 51))
        self.yes_2.setObjectName("yes_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(280, 170, 141, 16))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.yes_2.setText(_translate("Form", "中止"))
        self.label_2.setText(_translate("Form", "正在生成，请等待"))

    def into(self):
        self.yes_2.show()
        self.label_2.show()

    def out(self, next=None):
        self.yes_2.hide()
        self.label_2.hide()
        if next:
            next()

