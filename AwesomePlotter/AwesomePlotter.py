#!/usr/local/bin/python3

import sys
from enum import Enum

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QDesktopWidget, QAction, QFileDialog, QInputDialog
from PyQt5 import QtGui

from Widgets.AwesomeDataReader import AwesomeDataReader
from Widgets.AwesomeSessionRecorder import AwesomeSessionRecorder

qss = """
QToolButton { 
    color: white; 
}
"""

class AwsPlotterState(Enum):
    PLAYING = 0
    RECORDING = 1

class AwesomePlotter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.width = 1200
        self.height = 800
        self.title = 'Awesome Data Reader (mais agents de la paix avant tout)'
        self.state = AwsPlotterState.PLAYING
        self.awsdr = None
        self.awssr = None
        self.initUI()

    def initUI(self):
        widget = QWidget(self)
        self.setCentralWidget(widget)
        self.mainLayout = QVBoxLayout(widget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.setupToolbar()

        # Inflate with reader by default
        #self.instantiateAwsdr()
        self.instantiateAwssr("Session0")
        self.inflateMainWidget(self.awssr)

        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, self.width, self.height)
        self.centerWindow()
        self.show()

    def centerWindow(self):
        qr = self.frameGeometry()
        qr.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(qr.topLeft())
    
    def setupToolbar(self):
        recordModeAct = QAction('Record Mode', self)
        recordModeAct.triggered.connect(self.enableRecordingMode)
        fileModeAct = QAction('Open LogFile', self)
        fileModeAct.triggered.connect(self.enableFileImportMode)

        self.toolbar = self.addToolBar('Main Toolbar')
        self.toolbar.setMovable(False)
        self.toolbar.addAction(fileModeAct)
        self.toolbar.addAction(recordModeAct)

    def inflateMainWidget(self, widget):
        self.mainLayout.addWidget(widget)

    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","CSV Files (*.csv)", options=options)
        return fileName

    def openRecordCreationDialog(self):
        projectName, ok = QInputDialog.getText(self, 'Session Creation', 'Enter the session name:')
        if ok:
            print('Creating the ' + str(projectName) + ' project...')
        return projectName, ok

    def launchAwsdrFileImport(self):
        filename = self.openFileDialog()
        if filename:
            self.awsdr.importFile(filename)
            self.state = AwsPlotterState.PLAYING

    def instantiateAwsdr(self):
        self.awsdr = AwesomeDataReader()

    def instantiateAwssr(self, sessionName):
        self.awssr = AwesomeSessionRecorder(sessionName)

    # MARK : Actions callbacks

    def enableRecordingMode(self):
        if self.state is AwsPlotterState.PLAYING:
            print('Engaging recording mode...')
            projectName, isValid = self.openRecordCreationDialog()
            if not isValid:
                return
            self.awsdr.closeWidget()
            if self.awsdr is None:
                self.instantiateAwssr()
            self.awssr = AwesomeSessionRecorder(projectName)
            self.inflateMainWidget(self.awssr)
        elif self.state is AwsPlotterState.RECORDING:
            pass
        
    def enableFileImportMode(self):
        print('Engaging file import mode...')
        if self.state is AwsPlotterState.PLAYING:
            if self.awsdr is None:
                self.instantiateAwsdr()
            self.awsdr.clearSimulation()
            self.launchAwsdrFileImport()
        elif self.state is AwsPlotterState.RECORDING:
            self.awssr.closeWidget()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qss)
    awsp = AwesomePlotter()
    sys.exit(app.exec_())