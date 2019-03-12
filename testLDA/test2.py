# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test2.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Sorter(object):
    def __init__(self,Form):
        self.setupUi(Form)
        self.out()

    def setupUi(self, Form):
        self.yes = QtWidgets.QPushButton(Form)
        self.yes.setGeometry(QtCore.QRect(90, 317, 171, 51))
        self.yes.setObjectName("yes")
        self.no = QtWidgets.QPushButton(Form)
        self.no.setGeometry(QtCore.QRect(370, 320, 171, 51))
        self.no.setObjectName("no")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(270, 30, 81, 31))
        self.label.setObjectName("label")
        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setGeometry(QtCore.QRect(120, 80, 401, 151))
        self.listWidget.setObjectName("listWidget")
        #self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.docD_2 = QtWidgets.QLineEdit(Form)
        self.docD_2.setGeometry(QtCore.QRect(180, 260, 81, 31))
        self.docD_2.setObjectName("docD_2")
        self.docD_3 = QtWidgets.QLineEdit(Form)
        self.docD_3.setGeometry(QtCore.QRect(370, 260, 81, 31))
        self.docD_3.setObjectName("docD_3")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(110, 270, 61, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(290, 270, 71, 16))
        self.label_3.setObjectName("label_3")
        self.openFile_2 = QtWidgets.QPushButton(Form)
        self.openFile_2.setGeometry(QtCore.QRect(490, 260, 81, 31))
        self.openFile_2.setObjectName("openFile_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.yes.setText(_translate("Form", "确定"))
        self.no.setText(_translate("Form", "取消"))
        self.label.setText(_translate("Form", "已训练结果"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.docD_2.setText(_translate("Form", "100"))
        self.docD_3.setText(_translate("Form", ""))
        self.label_2.setText(_translate("Form", "评论数："))
        self.label_3.setText(_translate("Form", "保存路径："))
        self.openFile_2.setText(_translate("Form", "浏览"))

    def into(self):
        #重新加载加载

        self.yes.show()
        self.no.show()
        self.label.show()
        self.label_2.show()
        self.label_3.show()
        self.openFile_2.show()
        self.docD_2.show()
        self.docD_3.show()
        self.listWidget.show()


    def out(self,next=None):
        self.yes.hide()
        self.no.hide()
        self.label.hide()
        self.label_2.hide()
        self.label_3.hide()
        self.openFile_2.hide()
        self.docD_2.hide()
        self.docD_3.hide()
        self.listWidget.hide()
        if next:
            next()
