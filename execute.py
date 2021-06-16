from PyQt5.QtWidgets import (
    QApplication, QInputDialog, QWidget, QGridLayout, QPushButton, QLabel)
from main import *


class ShowResult(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.label = QLabel(str(), self)
        btn1 = QPushButton('Load', self)
        btn1.clicked.connect(self.loadFile)

        grid = QGridLayout()
        self.setLayout(grid)

        grid.addWidget(btn1, 0, 0)
        grid.addWidget(self.label, 1, 0)

        self.setWindowTitle('Result')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def loadFile(self):
        name, ok = QInputDialog.getText(self, 'File Loader', 'Input File Name')

        if ok:
            with open(name+".json", "r") as f:
                circuit = json.load(f)
            resultDict = rawToResult(circuit)  # 회로 json -> 결과 딕션 함수
            self.textSet(resultDict)

    def textSet(self, resultDict):
        text = str()
        for i in resultDict:
            text += i+" : "+str(resultDict[i]["value"])+"\n"
        self.label.setText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ShowResult()
    sys.exit(app.exec_())
