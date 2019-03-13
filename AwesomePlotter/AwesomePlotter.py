#!/usr/local/bin/python3

import sys
from enum import Enum

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QDesktopWidget, QAction, QFileDialog, QInputDialog

from Widgets.AwesomeDataReader import AwesomeDataReader

qss = """
QToolButton { 
    color: white; 
}
"""

class AwsStatusState(Enum):
    PLAYING = 0
    RECORDING = 1

class AwesomePlotter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.width = 1200
        self.height = 800
        self.title = 'Awesome Data Reader (mais agents de la paix avant tout)'
        self.state = AwsStatusState.PLAYING
        self.initUI()

    def initUI(self):
        widget = QWidget(self)
        self.setCentralWidget(widget)
        self.mainLayout = QVBoxLayout(widget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.setupToolbar()

        self.awsdr = AwesomeDataReader()
        self.mainLayout.addWidget(self.awsdr)

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
        recordModeAct.triggered.connect(self.enableRecordMode)
        fileModeAct = QAction('Open LogFile', self)
        fileModeAct.triggered.connect(self.enableFileImportMode)

        self.toolbar = self.addToolBar('Main Toolbar')
        self.toolbar.setMovable(False)
        self.toolbar.addAction(fileModeAct)
        self.toolbar.addAction(recordModeAct)

    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","CSV Files (*.csv)", options=options)
        return fileName

    def openRecordCreationDialog(self):
        projectName, ok = QInputDialog.getText(self, 'Session Creation', 'Enter the session name:')
        if ok:
            print('Creating the ' + str(projectName) + ' project...')

    def launchImport(self):
        filename = self.openFileDialog()
        if filename:
            self.awsdr.importFile(filename)
            self.state = AwsStatusState.PLAYING

    def enableRecordMode(self):
        print('Engaging recording mode...')
        self.openRecordCreationDialog()
        
    def enableFileImportMode(self):
        print('Engaging file import mode...')
        if self.state is AwsStatusState.PLAYING:
            self.awsdr.clearSimulation()
            self.launchImport()
        elif self.state is AwsStatusState.RECORDING:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qss)
    awsp = AwesomePlotter()
    sys.exit(app.exec_())