#!/usr/local/bin/python3

from enum import Enum

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5 import QtGui

from Widgets.WidgetRecorderPlotter import WidgetRecorderPlotter

class AwsRecorderState(Enum):
    IDLE = 0
    RECORDING = 1

class AwesomeSessionRecorder(QWidget):
    def __init__(self, sessionName):
        super().__init__()
        print("Opening AWSSR...")
        self.sessionName = sessionName
        self.state = AwsRecorderState.IDLE
        self.initUI()

    def initUI(self):
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        label = self.setupProjectNameLabel()
        self.mainLayout.addWidget(label)

        self.graph = WidgetRecorderPlotter()
        self.mainLayout.addWidget(self.graph)

        self.setupEventButton()

        commandPanelLayout = self.setupCommandPanel()
        self.mainLayout.addLayout(commandPanelLayout)

        self.show()

    def setupProjectNameLabel(self):
        label = QLabel()
        font = QtGui.QFont(str(QtGui.QFont().defaultFamily()), 32, QtGui.QFont.Bold)
        label.setFont(font)
        label.setText(self.sessionName)
        label.setMargin(10)
        return label

    def setupEventButton(self):
        self.eventButton = QPushButton('Event', self)
        self.eventButton.clicked[bool].connect(self.logEvent)
        self.eventButton.setShortcut("Space")
        self.mainLayout.addWidget(self.eventButton)

    def setupCommandPanel(self):
        panelLayout = QHBoxLayout()
        self.playButton = QPushButton('Play', self)
        self.stopButton = QPushButton('Stop', self)
        self.clearButton = QPushButton('Clear', self)
        self.saveButton = QPushButton('Save', self)
        self.playButton.clicked[bool].connect(self.launchRecord)
        self.stopButton.clicked[bool].connect(self.stopRecord)
        self.clearButton.clicked[bool].connect(self.clearRecord)
        self.saveButton.clicked[bool].connect(self.saveRecord)

        panelLayout.addWidget(self.playButton)
        panelLayout.addWidget(self.stopButton)
        panelLayout.addWidget(self.clearButton)
        panelLayout.addWidget(self.saveButton)

        return panelLayout

    def closeWidget(self):
        print("Closing AWSSR...")
        self.close()

    # MARK : Actions callbacks

    def logEvent(self):
        if self.state is AwsRecorderState.RECORDING:
            self.graph.logEvent()
            print('New event logged at t=' + str(self.graph.getActualTime()))

    def launchRecord(self):
        if self.state is AwsRecorderState.IDLE:
            print('Starting record...')
            self.state = AwsRecorderState.RECORDING
            self.graph.startRecording()
    
    def stopRecord(self):
        if self.state is AwsRecorderState.RECORDING:
            print('Stoping record...')
            self.state = AwsRecorderState.IDLE
            self.graph.stopRecording()

    def clearRecord(self):
        if self.state is AwsRecorderState.RECORDING:
            self.stopRecord()
        print('Clearing record...')
        self.graph.clearRecording()

    def saveRecord(self):
        print('Saving record...')

    # MARK : IGraphicalUpdateHandler callbacks

    def onGraphUpdate(self, point, time):
        print('BIP')