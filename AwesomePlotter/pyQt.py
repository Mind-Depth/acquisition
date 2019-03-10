#!/usr/local/bin/python3

import sys
 
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QHBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QDesktopWidget, QAction
from PyQt5.QtGui import QIcon, QFont
 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import random

qss = """
QToolButton { 
    color: white; 
}
"""

class WidgetPlot(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.canvas = Plotter(self, width=10, height=8)
        self.layout().addWidget(self.canvas)

class Plotter(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.initUI()

    def initUI(self):
        ax = self.figure.add_subplot(111)
        ax.set_xlabel('Time')
        ax.set_ylabel('BPM')

class AwesomePlotter(QMainWindow):

    def __init__(self):
        super().__init__()
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
        self.playButton.clicked[bool].connect(self.launchSimulation)
        self.stopButton.clicked[bool].connect(self.stopSimulation)

        hbox.addWidget(self.playButton)
        hbox.addWidget(self.stopButton)
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

    def centerWindow(self):
        qr = self.frameGeometry()
        qr.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(qr.topLeft())

    def launchSimulation(self):
        source = self.sender()
        source.setText('Pause')
        print('Launching simulation...')

    def stopSimulation(self):
        self.playButton.setText('Play')
        print('Stopping simulation...')

    def enableBleMode(self):
        print('Engaging bluetooth mode...')

    def enableFileImportMode(self):
        print('Engaging file import mode...')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qss)
    ex = AwesomePlotter()
    sys.exit(app.exec_())