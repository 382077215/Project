from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QFileDialog
import threading
from test2 import *
from test3 import *
from test4 import *
from test5 import *
from test6 import *

_translate = QtCore.QCoreApplication.translate

class MW(QtWidgets.QMainWindow):

    def __init__(self):
        super(MW,self).__init__()

        self.setObjectName("KIC")
        self.resize(640, 431)
        self.setWindowTitle("KIC")
        self.setWindowFlags(QtCore.Qt.WindowFullscreenButtonHint)
        self.setFixedSize(self.width(), self.height())

        self.welcome = Welcome(self)
        self.trainer = Trainer(self)
        self.sorter = Sorter(self)
        self.wait1 = Wait1(self)
        self.wait2 = Wait2(self)

        self.welcome.exit.clicked.connect(self.close)
        self.welcome.sortD.clicked.connect(lambda _:self.welcome.out(self.sorter.into))
        self.welcome.trainM.clicked.connect(lambda _:self.welcome.out(self.trainer.into))

        self.trainer.cancel.clicked.connect(lambda _:self.trainer.out(self.welcome.into))
        self.sorter.no.clicked.connect(lambda _:self.sorter.out(self.welcome.into))

        self.wait1.yes_2.clicked.connect(lambda _:self.wait1.out(self.trainer.into))
        self.wait2.yes_2.clicked.connect(lambda _:self.wait2.out(self.sorter.into))

        self.trainer.chooseFile.clicked.connect(lambda _:self.loadFile("",self.trainer.inputData))
        self.trainer.openFile.clicked.connect(lambda _:self.saveFile1("",self.trainer.targetData))
        self.trainer.yes.clicked.connect(lambda _:self.trainer.out(self.wait1.into) if self.trainer.inputData.text() and self.trainer.targetData.text() else None)

        self.sorter.yes.clicked.connect(self.sortPL)
        self.sorter.openFile_2.clicked.connect(lambda _:self.saveFile2("",self.sorter.docD_3))

        self.welcome.into()

    def runModel(self):
        import pandas as pd
        import numpy as np
        import re

        v = re.compile("【.*?】")
        plun = pd.read_excel("D:/outdata.xlsx", sheetname="outdata")
        doctop = pd.read_excel("D:/outdata.xlsx", sheetname="doctop")
        topter = pd.read_excel("D:/outdata.xlsx", sheetname="topter")

        M1 = plun["text"].map(lambda _: "".join(v.split(str(_))))
        M1 = M1.map(lambda _: [topter[w] for w in _.strip().split() if w and w in topter.columns])
        M1 = M1.map(lambda _: [sum(__) for __ in zip(*_)] if _ else [0, 0, 0, 0, 0])

        M2 = plun["id"].map(lambda _: doctop.loc[_])
        M2 = M2.map(lambda _: _ * np.log2(_))
        M3 = plun["text"].map(lambda _: len(set(str(_).strip().split())))

        M4 = list(map(lambda x, y, z: -z * sum([xx * yy for xx, yy in zip(x, y)]), M1, M2, M3))
        plun["score"] = M4
        plun.sort_values("score", ascending=False, inplace=True)

    def getPL(self,sourcePath,targetPath,size):
        import time,openpyxl,csv
        sourcePath = sourcePath[sourcePath.find('(')+1:-1]
        time.sleep(0.5)
        if size:
            size = int(size)
        if sourcePath.strip() and targetPath.strip():
            try:
                TfileType = targetPath.split('.')[-1]

                if TfileType == 'csv':
                    with open(sourcePath, 'r+') as s:
                        with open(targetPath, 'w', newline='') as t:
                            sreader = csv.reader(s)
                            treader = csv.writer(t)
                            for ind, item in enumerate(sreader):
                                if ind > size:
                                    break
                                else:
                                    treader.writerow(item)
                else:
                    with open(sourcePath, 'r+') as s:
                        sreader = csv.reader(s)
                        tf = openpyxl.Workbook()
                        ws = tf.active
                        ws.title = 'DATA'
                        for row, item in enumerate(sreader):
                            if row > size:
                                break
                            for ind, val in enumerate(item):
                                ws.cell(column=ind + 1, row=row + 1, value=val)
                        try:
                            tf.save(filename=targetPath)
                        finally:
                            tf.close()
            finally:
                self.wait2.out(self.sorter.into)
        #self.openDir("/".join(targetPath.split("/")[:-1]))

    def sortPL(self):
        if self.sorter.listWidget.selectedItems() and self.sorter.docD_3.text().strip() and self.sorter.docD_2.text().strip().isdigit():
            self.sorter.out(self.wait2.into)
            t = threading.Thread(target=lambda: self.getPL(
                self.sorter.listWidget.selectedItems()[0].text(),
                self.sorter.docD_3.text(),
                self.sorter.docD_2.text()), name="PLThread")
            t.start()

    def addNewRes(self,path):
        fileName = path.strip().split("/")[-1].split('.')[0]
        item = QtWidgets.QListWidgetItem("{0}({1})".format(fileName,path),self.sorter.listWidget)
        self.sorter.listWidget.addItem(item)






    def openDir(self,path):
        QDesktopServices.openUrl(QUrl('file:///' + path))

    def loadFile(self,path,showText):
        showText.setText(QFileDialog.getOpenFileName(self, "打开", path,filter="Excel文件(*.xlsx *.xls);;csv文件(*.csv)")[0])

    def saveFile2(self,path,showText):
        showText.setText(QFileDialog.getSaveFileName(self, "打开", path,filter="Excel文件(*.xlsx);;Excel文件(*.xls);;csv文件(*.csv)")[0])

    def saveFile1(self, path, showText):
        showText.setText(
            QFileDialog.getSaveFileName(self, "打开", path, filter="csv文件(*.csv)")[0])


if __name__ == '__main__':
    import sys,os
    app = QtWidgets.QApplication(sys.argv)
    widget = MW()
    with open("save","r") as f:
        lines = [save for save in f.readlines() if save.strip() and os.path.exists(save)]
        [widget.addNewRes(save) for save in lines]
    with open("save", "w") as f:
        f.writelines(lines)
    widget.show()
    app.exec_()
    #保存内存中的记录
    sys.exit()