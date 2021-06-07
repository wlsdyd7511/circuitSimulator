import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QPushButton, QLabel, QInputDialog)
import json


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.res = str()
        self.cnt = {
                    "DCPower" : 0,
                    "resistor" : 0,
                    "diode" : 0
                   }

    def initUI(self):
        btn1 = QPushButton('DCPower', self)
        btn1.clicked.connect(self.showDialog('DCPower'))
        btn2 = QPushButton('resister', self)
        btn2.clicked.connect(self.showDialog('Resister'))
        btn3 = QPushButton('diode', self)
        btn3.clicked.connect(self.showDialog('Diode'))
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

    def showDialog(self, type):
        if type == 'DCPower':
            value, ok = QInputDialog.getText(
                self, 'Input Votage', "Enter Voltage")

            if ok:
                pin1, ok = QInputDialog.getText(
                    self, 'Input Pin', "Enter Pin in Tuple")

                if ok:
                    self.cnt[0] += 1
                    self.res += "DCPower"+str(self.cnt)+" : "+value+"V"+"\n"
                    self.label.setText(self.res)

        if type == 'resistor':
            value, ok = QInputDialog.getText(
                self, 'Input Value', "Enter Value")

            if ok:
                text, ok = QInputDialog.getText(
                    self, 'Input Pin', "Enter Pin in Tuple")

                if ok:
                    self.res += "Resister"+str(self.cnt)+" : "+value+"Ω"+"\n"
                    self.label.setText(self.res)
                    self.cnt[1] += 1

        if type == 'Diode':
            value, ok = QInputDialog.getText(
                self, 'Input Value', "Enter Value")

            if ok:
                text, ok = QInputDialog.getText(
                    self, 'Input Pin', "Enter Pin in Tuple")

                if ok:
                    self.res += "Diode" + "\n"
                    self.label.setText(self.res)
                    self.cnt[2] += 1

        self.formDict(self, rawCircuit, type, self.cnt, float(value),)

    def formDict(self, rawCircuit, type, cnt, value, pin):  # (self, dict, str, int, float, list)
        key = type + str(cnt[type])
        rawCircuit[key] = dict()
        rawCircuit[key]["type"] = type
        if type == "DCPower":
            rawCircuit[key]["voltage"] = value
        elif type == "resistor":
            rawCircuit[key]["resistance"] = value
        rawCircuit[key]["pin"] = pin
        return rawCircuit


if __name__ == '__main__':
    rawCircuit = dict()
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
