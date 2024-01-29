import os
import psutil
import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
import subprocess
import json

jsonFile = "D:/Users/Kevin/Documents/python/BlueButton/appsList.json"
STYLESHEET = """
QWidget {
    background-color: grey;
}
QPushButton {
    background-color: lightblue;
}
QLineEdit {
    background-color: white;
}
"""

def readJsonFile(jsonFile):
    with open(jsonFile, 'r') as readFile:
        data = json.load(readFile)
    return data


class ApplicationLauncher(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ApplicationLauncher, self).__init__(parent=parent)
        self.initUI()

    def initUI(self):
        outerLayout = QtWidgets.QVBoxLayout()
        topLayout = QtWidgets.QFormLayout()
        search_bar = QtWidgets.QLineEdit()
        topLayout.addRow("Search: ", search_bar)
        buttonLayout = QtWidgets.QVBoxLayout()
        jsonData = readJsonFile(jsonFile)
        for entry in jsonData:
            buttonName = (entry.get("name"))
            exePath = (entry.get("path"))
            icon = (entry.get("icon"))
            buttonInst = QtWidgets.QPushButton(buttonName)
            buttonInst.setIcon(QIcon(icon))
            buttonInst.setProperty("appPath", exePath)
            buttonInst.setToolTip("Click to launch " + buttonName)
            buttonLayout.addWidget(buttonInst)
            buttonInst.clicked.connect(self.launchApp)
            #print(exePath)
            #print(buttonInst)

        outerLayout.addLayout(topLayout)
        outerLayout.addLayout(buttonLayout)
        self.setLayout(outerLayout)
        self.setWindowTitle("Blue Button")
        self.setMinimumWidth(190)
        self.setMinimumHeight(190)
        self.show()

    def launchApp(self):
        button = self.sender()
        #print(button.property("appPath"))
        path = button.property("appPath")
        exe = os.path.split(path)[1]
        if exe not in (p.name() for p in psutil.process_iter()):
            result = subprocess.Popen(
                path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True)
        else:
            prompt = QtWidgets.QMessageBox.question(
                self,
                "Oops!",
                "{} is already running! Do you want to open another instance?".format(exe),
                QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes)

            if prompt == QtWidgets.QMessageBox.Yes:
                result = subprocess.Popen(
                    path,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True)


class LaunchButton(QtWidgets.QPushButton):
    def __init__(self, applicationName, applicationPath, appIcon):
        super(LaunchButton, self).__init__()
        self.applicationPath = applicationPath
        self.appIcon = appIcon
        self.applicationName = applicationName


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    launcher = ApplicationLauncher()
    sys.exit(app.exec_())
