#!/usr/local/bin/python3

import sys
from enum import Enum

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QDesktopWidget, QAction, QFileDialog, QInputDialog
from PyQt5 import QtGui

from Widgets.AwesomeDataReader import AwesomeDataReader
from Widgets.AwesomeSessionRecorder import AwesomeSessionRecorder
from Widgets.ErrorDialog import ErrorDialog
from Utils.CsvUtils import getCsvFilesFromFolder

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
        self.instantiateAwsdr()
        self.inflateMainWidget(self.awsdr)

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
        folderPath = QFileDialog.getExistingDirectory(self, "Select Directory", options=options)
        if folderPath:
            csvList = getCsvFilesFromFolder(folderPath)
            return csvList
        else:
            return None

    def openRecordCreationDialog(self):
        self.state = AwsPlotterState.RECORDING
        projectName, ok = QInputDialog.getText(self, 'Session Creation', 'Enter the session name:')
        if ok:
            print('Creating the ' + str(projectName) + ' project...')
            self.awssr.loadSession(projectName)

    def launchAwsdrFileImport(self):
        self.state = AwsPlotterState.PLAYING
        files = self.openFileDialog()
        if not files:
            ErrorDialog(self, 'Your data folder must contain almost a bio.csv or a ev.csv file')
            return
        bioImported = False
        evImported = False
        for f in files:
            if str.__contains__(f, 'bio.csv'):
                bioImported = True
            elif str.__contains__(f, 'ev.csv'):
                evImported = True
        if bioImported or evImported:
            self.awsdr.importFile(files)
        else:
            ErrorDialog(self, 'Your data folder must contain almost a bio.csv or a ev.csv file')

    def instantiateAwsdr(self):
        self.awsdr = AwesomeDataReader()

    def instantiateAwssr(self):
        self.awssr = AwesomeSessionRecorder()

    # MARK : Actions callbacks

    def enableRecordingMode(self):
        print('Engaging recording mode...')
        if self.state is AwsPlotterState.RECORDING:
            self.awssr.clearRecord()
            self.openRecordCreationDialog()
        elif self.state is AwsPlotterState.PLAYING:
            self.awsdr.clearSimulation()
            self.awsdr.closeWidget()

            self.instantiateAwssr()
            self.inflateMainWidget(self.awssr)
            self.openRecordCreationDialog()
        
    def enableFileImportMode(self):
        print('Engaging file import mode...')
        if self.state is AwsPlotterState.PLAYING:
            self.awsdr.clearSimulation()
            self.launchAwsdrFileImport()
        elif self.state is AwsPlotterState.RECORDING:
            self.awssr.clearRecord()
            self.awssr.closeWidget()

            self.instantiateAwsdr()
            self.inflateMainWidget(self.awsdr)
            self.launchAwsdrFileImport()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qss)
    awsp = AwesomePlotter()
    sys.exit(app.exec_())