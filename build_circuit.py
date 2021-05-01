import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QPushButton, QLabel, QInputDialog)

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.res = ""
        self.cnt = 0
        self.resList = list()

    def initUI(self):
        btn1 = QPushButton('DCPower', self)
        btn1.clicked.connect(self.showDialogDC)
        btn2 = QPushButton('resister', self)
        btn2.clicked.connect(self.showDialogResister)
        btn3 = QPushButton('diode', self)
        btn3.clicked.connect(self.showDialogDiode)
        self.label = QLabel(self)


        grid = QGridLayout()
        self.setLayout(grid)

        grid.addWidget(btn1, 0, 0)
        grid.addWidget(btn2, 0, 1)
        grid.addWidget(btn3, 0, 2)
        grid.addWidget(self.label, 1, 1)

        self.setWindowTitle('Build Circuit')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def showDialogDCPower(self):
        text, ok = QInputDialog.getText(self, 'Input Votage', "Enter Voltage")

        if ok:
            self.resList.append(["DCPower"])
            self.resList[self.cnt].append(int(text))
            text, ok = QInputDialog.getText(self, 'Input Pin', "Enter Pin in Tuple")

            if ok:
                self.resList[self.cnt].append(tuple(text))
                self.res += "DCPower" + "\n"
                self.label.setText(self.res)
                self.cnt += 1


    def showDialogResister(self):
        text, ok = QInputDialog.getText(self, 'Input Value', "Enter Value")

        if ok:
            self.resList.append(["Resister"])
            self.resList[self.cnt].append(int(text))
            text, ok = QInputDialog.getText(self, 'Input Pin', "Enter Pin in Tuple")

            if ok:
                self.resList[self.cnt].append(tuple(text))
                self.res += "Resister" + "\n"
                self.label.setText(self.res)
                self.cnt += 1


    def showDialogDiode(self):
        text, ok = QInputDialog.getText(self, 'Input Value', "Enter Value")

        if ok:
            self.resList.append(["Diode"])
            self.resList[self.cnt].append(int(text))
            text, ok = QInputDialog.getText(self, 'Input Pin', "Enter Pin in Tuple")

            if ok:
                self.resList[self.cnt].append(tuple(text))
                self.res += "Diode" + "\n"
                self.label.setText(self.res)
                self.cnt += 1

