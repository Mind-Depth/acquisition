import sys
from enum import Enum

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox

from Widgets.WidgetReaderPlotter import WidgetReaderPlotter
from Widgets.ErrorDialog import ErrorDialog
from Utils.CsvUtils import loadCsv
from FearClassifier import FearClassifier
from Interfaces.IGraphicalUpdateHandler import IGraphicalUpdateHandler
from Interfaces.IAIBehaviourHandler import IAIBehaviourHandler
from Interfaces.IGraphicalUpdateHandler import IGraphicalUpdateHandlerFinalMeta

class AwsReaderState(Enum):
    IDLE = 0
    LOADED = 1
    PLAYING = 2
    PAUSED = 3

class AwesomeDataReader(QWidget, IGraphicalUpdateHandler, IAIBehaviourHandler, metaclass=IGraphicalUpdateHandlerFinalMeta):

    def __init__(self):
        super().__init__()
        print("Opening AWSDR...")
        self.state = AwsReaderState.IDLE
        self.ai = FearClassifier(handler=self)
        self.ai.trainIA()
        self.initUI()

    def initUI(self):
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.graph = WidgetReaderPlotter(self)
        self.mainLayout.addWidget(self.graph)

        commandPanelLayout = self.setupCommandPanel()
        self.mainLayout.addLayout(commandPanelLayout)
        
        self.show()

    def closeWidget(self):
        self.close()

    def setupCommandPanel(self):
        hbox = QHBoxLayout()
        self.playButton = QPushButton('Play', self)
        self.stopButton = QPushButton('Stop', self)
        self.clearButton = QPushButton('Clear', self)
        self.playButton.clicked[bool].connect(self.launchSimulation)
        self.stopButton.clicked[bool].connect(self.stopSimulation)
        self.clearButton.clicked[bool].connect(self.clearSimulation)
        self.aiCb = QCheckBox('AI realtime analyse', self)
        self.aiCb.toggle()
        self.aiCb.stateChanged.connect(self.updateAiUsage)

        hbox.addWidget(self.playButton)
        hbox.addWidget(self.stopButton)
        hbox.addWidget(self.clearButton)
        hbox.addWidget(self.aiCb)
        return hbox

    def plotAiSegments(self, loadedData):
        segments = self.ai.getFearSegments(loadedData)    
        for segment in segments:
            self.graph.plotPolyline(segment, color='-r')

    def updateAiUsage(self, state):
        if self.state is AwsReaderState.PLAYING or self.state is AwsReaderState.PAUSED:
            ErrorDialog(self, 'Unable to disable AIRT while reading, please stop the reading and try again')
            if not state:
                self.aiCb.setChecked(Qt.Checked)
            else:
                self.aiCb.setChecked(Qt.Unchecked)
            return
        if state == Qt.Checked:
            print("AIRT enabled...")
        else:
            print("AIRT disabled...")

    def importFile(self, fileName):
        if self.state is not AwsReaderState.IDLE:
            self.graph.clearData()
        loadedData = loadCsv(fileName)
        self.graph.loadData(loadedData)
        self.graph.plotData()
        self.plotAiSegments(loadedData)
        self.state = AwsReaderState.LOADED

    def closeWidget(self):
        print("Closing AWSDR...")
        self.close()

    ### MARK : IAIBehaviourHandler callbacks ###

    def onIaHasPredicted(self, segmentBuff):
        self.graph.plotPolyline(segmentBuff, '-r')

    ### MARK : IGraphicalUpdateHandler callbacks ###

    def onGraphUpdate(self, point, time):
        if self.aiCb.isChecked():
            self.ai.addPoint(point, time)

    ### MARK : Actions callbacks ###

    def launchSimulation(self):
        source = self.sender()
        if self.state is AwsReaderState.PAUSED:
            print('Resuming simulation...')
            self.state = AwsReaderState.PLAYING
            source.setText('Pause')
            self.graph.resumeMockPlaying()
        elif self.state is AwsReaderState.PLAYING:
            print('Pausing simulation...')
            self.state = AwsReaderState.PAUSED
            source.setText('Play')
            self.graph.pauseMockPlaying()
        elif self.state is AwsReaderState.IDLE:
            ErrorDialog(self, 'Please, load datas or connect a BLE device before launching the simulation')
        else:
            print('Launching simulation...')
            self.state = AwsReaderState.PLAYING
            source.setText('Pause')
            self.graph.clearData()
            self.graph.launchMockPlaying()
        
    def stopSimulation(self):
        if self.state is AwsReaderState.PLAYING or self.state is AwsReaderState.PAUSED:
            print('Stopping simulation...')
            self.playButton.setText('Play')
            self.graph.stopMockPlaying()
            self.graph.plotData()
            self.plotAiSegments(self.graph.getLoadedData())
            self.ai.flushCurrentData()
            self.state = AwsReaderState.LOADED
        
    def clearSimulation(self):
        if self.state is not AwsReaderState.IDLE:
            if self.state is AwsReaderState.PLAYING or self.state is AwsReaderState.PAUSED:
                self.stopSimulation()
            print('Clearing simulation...')
            self.graph.clearData()
            self.ai.flushCurrentData()
            self.playButton.setText('Play')
            self.state = AwsReaderState.IDLE