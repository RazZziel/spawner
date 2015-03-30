import subprocess
from PyQt5.QtCore import (QObject, pyqtSignal, qDebug, QTimer, QProcess)

def print(stuff): qDebug(stuff)

class Hatchling(QObject):

    gotOutput = pyqtSignal(str)

    def __init__(self, index, cmd):
        super(Hatchling, self).__init__()

        self.index = index
        self.cmd = cmd

        self._actualCmd = self.cmd.replace("{}", str(self.index+1))
        print("Created hatchling %d (%s)" % (self.index, self._actualCmd))

        self.startProcess()

    def startProcess(self):
        #self.process = subprocess.Popen(["bash", "-c", self._actualCmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #self._checkOutputTimer = QTimer()
        #self._checkOutputTimer.timeout.connect(self.checkOutput)
        #self._checkOutputTimer.start(1000)

        self.process = QProcess(self)
        #self.process.readyRead.connect(self.checkOutput)
        self.process.readyReadStandardOutput.connect(self.checkStdout)
        self.process.readyReadStandardError.connect(self.checkStderr)
        #self.process.setProcessChannelMode(QProcess.ForwardedChannels)
        #self.process.finished.connect(startProcess)
        self.process.start("bash", ["-c", self._actualCmd])

    def checkOutput(self):
        print("~readyRead");
        self.gotOutput.emit(self.process.readAll().data().decode("utf-8"))
        #self.gotOutput.emit(self.process.stdout.read())
        #self.gotOutput.emit(self.process.stderr.read())

    def checkStdout(self):
        self.gotOutput.emit(self.process.readAllStandardOutput().data().decode("utf-8"))

    def checkStderr(self):
        self.gotOutput.emit(self.process.readAllStandardError().data().decode("utf-8"))

    def __del__(self):
        print("Stopping hatchling %d (%s)" % (self.index, self._actualCmd))

        #self.process.terminate()
        #try:
        #    self.process.wait(1)
        #except subprocess.TimeoutExpired as e:
        #    print("Killing hatchling %d (%s)" % (self.index, self._actualCmd))
        #    self.process.kill()
        #    try:
        #        self.process.wait(1)
        #    except subprocess.TimeoutExpired as e:
        #        print("!! Could not stop process: %s" % e)

        self.process.terminate()
        if not self.process.waitForFinished(1000):
            print("Killing hatchling %d (%s)" % (self.index, self._actualCmd))
            self.process.kill()


class Hatchery(QObject):

    cmd = ""
    numInstances = 0

    gotOutput = pyqtSignal(str)

    _instances = []


    def __init__(self):
        super(Hatchery, self).__init__()

    def isValidInstance(self, instance):
        return instance.cmd == self.cmd and instance.index <= self.numInstances

    def update(self):

        self._instances = list(filter(self.isValidInstance, self._instances))

        # Creating instances
        if len(self._instances) < self.numInstances and len(self.cmd) > 0:
            for i in range(len(self._instances), self.numInstances):
                print("Adding instance %d" % i)
                hatchling = Hatchling(i, self.cmd)
                hatchling.gotOutput.connect(self.gotOutput)
                self._instances.append(hatchling)

    def killAll(self):
        del self._instances[:]

    def setCmd(self, cmd):
        self.cmd = cmd
        self.update()

    def setNumInstances(self, numInstances):
        self.numInstances = numInstances
        self.update()