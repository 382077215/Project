# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test4.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Trainer(object):
    def __init__(self,Form):
        self.setupUi(Form)
        self.out(None)
    def setupUi(self, Form):
        self.cancel = QtWidgets.QPushButton(Form)
        self.cancel.setGeometry(QtCore.QRect(370, 280, 171, 51))
        self.cancel.setObjectName("cancel")
        self.yes = QtWidgets.QPushButton(Form)
        self.yes.setGeometry(QtCore.QRect(90, 277, 171, 51))
        self.yes.setObjectName("yes")
        self.inputData = QtWidgets.QLineEdit(Form)
        self.inputData.setGeometry(QtCore.QRect(170, 60, 281, 51))
        self.inputData.setObjectName("inputData")
        self.chooseFile = QtWidgets.QPushButton(Form)
        self.chooseFile.setGeometry(QtCore.QRect(470, 60, 101, 51))
        self.chooseFile.setObjectName("chooseFile")

        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(70, 70, 91, 20))
        self.label.setObjectName("label")
        self.zhuti = QtWidgets.QLineEdit(Form)
        self.zhuti.setGeometry(QtCore.QRect(190, 190, 81, 31))
        self.zhuti.setObjectName("zhuti")
        self.modelD = QtWidgets.QLineEdit(Form)
        self.modelD.setGeometry(QtCore.QRect(440, 230, 81, 31))
        self.modelD.setObjectName("modelD")
        self.diedai = QtWidgets.QLineEdit(Form)
        self.diedai.setGeometry(QtCore.QRect(190, 230, 81, 31))
        self.diedai.setObjectName("diedai")
        self.docD = QtWidgets.QLineEdit(Form)
        self.docD.setGeometry(QtCore.QRect(440, 190, 81, 31))
        self.docD.setObjectName("docD")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(110, 200, 72, 15))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(110, 240, 72, 15))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(330, 200, 101, 20))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(330, 230, 101, 20))
        self.label_5.setObjectName("label_5")
        self.targetData = QtWidgets.QLineEdit(Form)
        self.targetData.setGeometry(QtCore.QRect(170, 130, 281, 51))
        self.targetData.setObjectName("targetData")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(70, 140, 91, 20))
        self.label_6.setObjectName("label_6")
        self.openFile = QtWidgets.QPushButton(Form)
        self.openFile.setGeometry(QtCore.QRect(470, 130, 101, 51))
        self.openFile.setObjectName("openFile")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.cancel.setText(_translate("Form", "取消"))
        self.yes.setText(_translate("Form", "确定"))
        self.chooseFile.setText(_translate("Form", "选择文件夹"))
        self.label.setText(_translate("Form", "输入文件名："))
        self.zhuti.setText(_translate("Form", "5"))
        self.modelD.setText(_translate("Form", "0.1"))
        self.diedai.setText(_translate("Form", "20000"))
        self.docD.setText(_translate("Form", "0.02"))
        self.label_2.setText(_translate("Form", "主题数："))
        self.label_3.setText(_translate("Form", "迭代次数："))
        self.label_4.setText(_translate("Form", "文档先验分布："))
        self.label_5.setText(_translate("Form", "主题先验分布："))
        self.label_6.setText(_translate("Form", "输出文件名："))
        self.openFile.setText(_translate("Form", "浏览"))

    def into(self):
        self.cancel.show()
        self.label_3.show()
        self.label.show()
        self.label_2.show()
        self.label_4.show()
        self.label_6.show()
        self.label_5.show()
        self.yes.show()
        self.targetData.show()
        self.openFile.show()
        self.docD.show()
        self.diedai.show()
        self.zhuti.show()
        self.chooseFile.show()
        self.inputData.show()
        self.modelD.show()

    def out(self,next=None):
        self.cancel.hide()
        self.label_3.hide()
        self.label.hide()
        self.label_2.hide()
        self.label_4.hide()
        self.label_6.hide()
        self.label_5.hide()
        self.yes.hide()
        self.targetData.hide()
        self.openFile.hide()
        self.docD.hide()
        self.diedai.hide()
        self.zhuti.hide()
        self.chooseFile.hide()
        self.inputData.hide()
        self.modelD.hide()

        if next:
            next()


