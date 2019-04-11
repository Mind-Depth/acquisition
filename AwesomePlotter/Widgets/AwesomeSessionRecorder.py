#!/usr/local/bin/python3

from enum import Enum

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5 import QtGui

from Widgets.WidgetRecorderPlotter import WidgetRecorderPlotter
from Widgets.ErrorDialog import ErrorDialog
from Controllers.SessionRecorderController import SessionRecorderController

class AwsRecorderState(Enum):
    IDLE = 0
    READY = 1
    RECORDING = 2

class AwesomeSessionRecorder(QWidget):
    def __init__(self):
        super().__init__()
        print("Opening AWSSR...")
        self.state = AwsRecorderState.IDLE
        self.initUI()

    def initUI(self):
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.sessionLabel = self.setupProjectNameLabel("Nameless Session")
        self.mainLayout.addWidget(self.sessionLabel)

        self.graph = WidgetRecorderPlotter()
        self.mainLayout.addWidget(self.graph)

        self.setupEventButton()

        commandPanelLayout = self.setupCommandPanel()
        self.mainLayout.addLayout(commandPanelLayout)

        self.show()

    def setupProjectNameLabel(self, projectName):
        label = QLabel()
        font = QtGui.QFont(str(QtGui.QFont().defaultFamily()), 32, QtGui.QFont.Bold)
        label.setFont(font)
        label.setText(projectName)
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
        self.playButton.setCheckable(True)
        self.stopButton = QPushButton('Stop', self)
        self.clearButton = QPushButton('Save and Clear', self)
        self.playButton.clicked[bool].connect(self.launchRecord)
        self.stopButton.clicked[bool].connect(self.stopRecord)
        self.clearButton.clicked[bool].connect(self.clearRecord)

        panelLayout.addWidget(self.playButton)
        panelLayout.addWidget(self.stopButton)
        panelLayout.addWidget(self.clearButton)

        return panelLayout

    def loadSession(self, sessionName):
        self.sessionName = sessionName
        self.sessionRecorder = SessionRecorderController(sessionName)
        self.sessionRecorder.createEnv()
        self.sessionLabel.setText(sessionName)
        self.state = AwsRecorderState.READY

    def closeWidget(self):
        print("Closing AWSSR...")
        self.close()

    # MARK : Actions callbacks

    def logEvent(self):
        if self.state is AwsRecorderState.RECORDING:
            self.graph.logEvent()
            self.sessionRecorder.addEvent(self.graph.getActualTime())
            print('New event logged at t=' + str(self.graph.getActualTime()))

    def launchRecord(self):
        if self.state is AwsRecorderState.READY:
            print('Starting record...')
            ErrorDialog(self, 'Warning : The BLE module is curently disconnected')
            self.state = AwsRecorderState.RECORDING
            self.graph.startRecording()
    
    def stopRecord(self):
        if self.state is AwsRecorderState.RECORDING:
            print('Stoping record...')
            self.playButton.setChecked(False)
            self.state = AwsRecorderState.READY
            self.graph.stopRecording()

    def clearRecord(self):
        if self.state is not AwsRecorderState.IDLE:
            if self.state is AwsRecorderState.RECORDING:
                self.stopRecord()
            print('Clearing record...')
            self.sessionRecorder.saveData()
            self.graph.clearRecording()
            self.sessionRecorder.flushData()