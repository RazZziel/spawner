#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import (Qt, pyqtSlot, qDebug)
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.uic import loadUi
from ui_spawner import Ui_Spawner
from hatchery import Hatchery

def print(stuff): qDebug(stuff)

class Spawner(QMainWindow):
    
    def __init__(self):
        super(Spawner, self).__init__()
        
        self.initUI()
        self.hatchery = Hatchery()

        self.hatchery.gotOutput.connect(self.updateOutput)
        
    def initUI(self):

        #self.ui = Ui_Spawner()
        #self.ui.setupUi(self)
        self.ui = loadUi('ui_spawner.ui', self)

        #self.ui.txtCmd.setText("while :; do echo {}; sleep {}; done")
        self.ui.txtCmd.setText("ping 192.168.1.{}")

    def closeEvent(self, event):
        self.hatchery.killAll()

    @pyqtSlot(int)
    def on_sldNumInstances_valueChanged(self, value):
        self.ui.btnLaunch.setText("Launch %d instances" % value)
        #self.hatchery.setNumInstances(value)

    @pyqtSlot(str)
    def updateOutput(self, text):
        self.ui.txtOutput.appendPlainText(text)

    @pyqtSlot()
    def on_btnLaunch_clicked(self):
        self.hatchery.setNumInstances(self.ui.sldNumInstances.value())
        self.hatchery.setCmd(self.ui.txtCmd.text())

    @pyqtSlot()
    def on_btnStop_clicked(self):
        self.hatchery.killAll()


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    spawner = Spawner()
    spawner.show()

    sys.exit(app.exec_())
