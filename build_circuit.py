import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QPushButton, QLabel, QInputDialog)
from PyQt5.QtCore import QCoreApplication
import json


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.rawCircuit = dict()
        self.res = str()
        self.cnt = {
            "DCPower": 0,
            "resistor": 0,
            "diode": 0
        }
        self.valueName = {
            "DCPower": "voltage",
            "resistor": "resistance",
            "diode": "voltage"
        }
        self.unit = {
            "DCPower": "V",
            "resistor": "Ω",
            "diode": "V"
        }
        self.initUI()

    def initUI(self):
        btn1 = QPushButton('DCPower', self)
        btn1.clicked.connect(lambda: self.showDialog('DCPower'))
        btn2 = QPushButton('resistor', self)
        btn2.clicked.connect(lambda: self.showDialog('resistor'))
        btn3 = QPushButton('diode', self)
        btn3.clicked.connect(lambda: self.showDialog('diode'))
        self.label = QLabel(self)
        finBtn = QPushButton('finish', self)
        finBtn.clicked.connect(self.finDialog)

        grid = QGridLayout()
        self.setLayout(grid)

        grid.addWidget(btn1, 0, 0)
        grid.addWidget(btn2, 0, 1)
        grid.addWidget(btn3, 0, 2)
        grid.addWidget(self.label, 1, 1)
        grid.addWidget(finBtn, 2, 1)

        self.setWindowTitle('Build Circuit')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def showDialog(self, type):
        if type == 'DCPower':
            value, ok = QInputDialog.getText(
                self, 'Input Value', "Enter Voltage")

            if ok:
                rawPin, ok = QInputDialog.getText(
                    self, 'Input Pin', "Enter Pin >pin1,pin2<")

                if ok:
                    self.cnt[type] += 1

        if type == 'resistor':
            value, ok = QInputDialog.getText(
                self, 'Input Value', "Enter Resistance")

            if ok:
                rawPin, ok = QInputDialog.getText(
                    self, 'Input Pin', "Enter Pin >pin1,pin2<")

                if ok:
                    self.cnt[type] += 1

        if type == 'Diode':
            value, ok = QInputDialog.getText(
                self, 'Input Value', "Enter Foward Voltage")

            if ok:
                rawPin, ok = QInputDialog.getText(
                    self, 'Input Pin', "Enter Pin >pin1,pin2<")

                if ok:
                    self.cnt[type] += 1

        pin = rawPin.split(",")
        self.res += type + \
            str(self.cnt[type])+" : "+value+self.unit[type]+str(pin)+"\n"
        self.label.setText(self.res)
        self.rawCircuit = self.formDict(
            self.rawCircuit, type, float(value), pin)

    def finDialog(self):
        fileName, ok = QInputDialog.getText(
            self, 'Save File', 'File Name')
        if ok:
            self.genJson(fileName)

    def formDict(self, rawCircuit, type, value, pin):
        #       (self, dict, str, int, float, list)
        key = type + str(self.cnt[type])
        rawCircuit[key] = dict()
        rawCircuit[key]["type"] = type
        rawCircuit[key][self.valueName[type]] = value
        rawCircuit[key]["pin"] = pin
        return rawCircuit

    def genJson(self, fileName):
        with open(f"{fileName}.json", "w") as json_file:
            json.dump(self.rawCircuit, json_file, indent=4)
        QCoreApplication.instance().quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
