# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test3.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Welcome(object):
    def __init__(self,Form):
        self.setupUi(Form)
        self.out()

    def setupUi(self, Form):
        self.trainM = QtWidgets.QPushButton(Form)
        self.trainM.setGeometry(QtCore.QRect(270, 150, 93, 28))
        self.trainM.setObjectName("trainM")
        self.sortD = QtWidgets.QPushButton(Form)
        self.sortD.setGeometry(QtCore.QRect(270, 210, 93, 28))
        self.sortD.setObjectName("sortD")
        self.exit = QtWidgets.QPushButton(Form)
        self.exit.setGeometry(QtCore.QRect(270, 270, 93, 28))
        self.exit.setObjectName("exit")
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(220, 80, 191, 41))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.trainM.setText(_translate("Form", "训练模型"))
        self.sortD.setText(_translate("Form", "选择模型"))
        self.exit.setText(_translate("Form", "退出"))
        self.textBrowser.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">欢迎使用本软件</span></p></body></html>"))

    def into(self):
        self.trainM.show()
        self.sortD.show()
        self.exit.show()
        self.textBrowser.show()

    def out(self,next=None):
        self.textBrowser.hide()
        self.sortD.hide()
        self.exit.hide()
        self.trainM.hide()
        if next:
            next()