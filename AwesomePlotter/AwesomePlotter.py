#!/usr/local/bin/python3

import sys
from enum import Enum

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QHBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QDesktopWidget, QAction, QFileDialog
from PyQt5.QtGui import QIcon, QFont

from WidgetPlot import WidgetPlot
from ErrorDialog import ErrorDialog
from CsvReader import CsvReader

qss = """
QToolButton { 
    color: white; 
}
"""

class AwsPlotterState(Enum):
    IDLE = 0
    LOADED = 1
    PLAYING = 2
    PAUSED = 3
    BLE_CONNECTED = 4

class AwesomePlotter(QMainWindow):

    def __init__(self):
        super().__init__()
        self.state = AwsPlotterState.IDLE
        self.width = 1200
        self.height = 800
        self.title = 'Awesome Plotter (mais agents de la paix avant tout)'
        self.initUI()

    def initUI(self):
        widget = QWidget(self)
        self.setCentralWidget(widget)
        vlay = QVBoxLayout(widget)

        self.setupToolbar()

        self.graph = WidgetPlot(self)
        vlay.addWidget(self.graph)

        hbox = self.setupCommandPanel()
        vlay.addLayout(hbox)
        
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, self.width, self.height)
        self.centerWindow()
        self.show()

    def setupCommandPanel(self):
        hbox = QHBoxLayout()
        self.playButton = QPushButton('Play', self)
        self.stopButton = QPushButton('Stop', self)
        self.clearButton = QPushButton('Clear', self)
        self.playButton.clicked[bool].connect(self.launchSimulation)
        self.stopButton.clicked[bool].connect(self.stopSimulation)
        self.clearButton.clicked[bool].connect(self.clearSimulation)

        hbox.addWidget(self.playButton)
        hbox.addWidget(self.stopButton)
        hbox.addWidget(self.clearButton)
        return hbox

    def setupToolbar(self):
        bleModeAct = QAction('Bluetooth Mode', self)
        bleModeAct.triggered.connect(self.enableBleMode)
        fileModeAct = QAction('Open LogFile', self)
        fileModeAct.triggered.connect(self.enableFileImportMode)

        self.toolbar = self.addToolBar('Main Toolbar')
        self.toolbar.setMovable(False)
        self.toolbar.addAction(bleModeAct)
        self.toolbar.addAction(fileModeAct)

    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","CSV Files (*.csv)", options=options)
        if not fileName:
            ErrorDialog(self, 'Invalid File')
        return fileName

    def centerWindow(self):
        qr = self.frameGeometry()
        qr.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(qr.topLeft())

    ### MARK : Action callbacks ###

    def launchSimulation(self):
        source = self.sender()
        if self.state is AwsPlotterState.PAUSED:
            print('Resuming simulation...')
            self.state = AwsPlotterState.PLAYING
            source.setText('Pause')
            self.graph.resumeMockPlaying()
        elif self.state is AwsPlotterState.PLAYING:
            print('Pausing simulation...')
            self.state = AwsPlotterState.PAUSED
            source.setText('Play')
            self.graph.pauseMockPlaying()
        elif self.state is AwsPlotterState.IDLE:
            ErrorDialog(self, 'Please, load datas or connect a BLE device before launching the simulation')
        else:
            print('Launching simulation...')
            self.state = AwsPlotterState.PLAYING
            source.setText('Pause')
            self.graph.clearData()
            self.graph.launchMockPlaying()
        

    def stopSimulation(self):
        if self.state is AwsPlotterState.PLAYING:
            print('Stopping simulation...')
            self.playButton.setText('Play')
            self.graph.stopMockPlaying()
            self.graph.plotData()
            self.state = AwsPlotterState.LOADED
        
    def clearSimulation(self):
        if self.state is not AwsPlotterState.IDLE:
            print('Clearing simulation...')
            self.graph.clearData()
            self.playButton.setText('Play')
            self.state = AwsPlotterState.IDLE

    def enableBleMode(self):
        print('Engaging bluetooth mode...')
        
    def enableFileImportMode(self):
        print('Engaging file import mode...')
        if self.state is not AwsPlotterState.IDLE:
            self.graph.clearData()
        filename = self.openFileDialog()
        if filename:
            csvR = CsvReader(filename)
            loadedData = csvR.getData()
            self.graph.loadData(loadedData)
            self.graph.plotData()
            self.state = AwsPlotterState.LOADED

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qss)
    ex = AwesomePlotter()
    sys.exit(app.exec_())