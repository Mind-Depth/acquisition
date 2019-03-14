#!/usr/local/bin/python3

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QHBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QDesktopWidget, QAction, QFileDialog
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
import numpy as np 

from Plotters.ReaderPlotter import ReaderPlotter

class WidgetReaderPlotter(QWidget):
    def __init__(self, handler=None):
        QWidget.__init__(self)

        self.handler = handler
        self.canvas = ReaderPlotter(self)
        graphToolBar = NavigationToolbar(self.canvas, self)
        graphToolBar.setMovable(False)
        dockLayout = QVBoxLayout()
        dockLayout.setMenuBar(graphToolBar)
        self.setLayout(dockLayout)
        self.layout().addWidget(self.canvas)
        self.iterCount = 0
        
    def loadData(self, data):
        self.loadedData = data
    
    def loadEvents(self, events):
        self.loadedEvents = events

    def getLoadedData(self):
        return self.loadedData

    def plotData(self):
        self.plotPolyline(self.loadedData)

    def plotEvents(self):
        for event in self.loadedEvents:
            self.canvas.plotEvents(event)

    def plotPolyline(self, buff, color='-b'):
        self.canvas.plotData(buff, color)

    def plotPoint(self, point):
        self.canvas.plotPoint(point, self.iterCount)

    def clearData(self):
        self.canvas.clearData()
        self.loadedData = []
        self.loadedEvents = []

    def launchMockPlaying(self):
        self.timer = self.canvas.new_timer(1000, [(self.updateCanvas, (), {})])
        self.timer.start()

    def stopMockPlaying(self):
        self.timer.stop()
        self.iterCount = 0
        self.clearData()
    
    def pauseMockPlaying(self):
        self.timer.stop()

    def resumeMockPlaying(self):
        self.timer.start()

    def updateCanvas(self):
        if self.handler is not None:
            self.handler.onGraphUpdate(self.loadedData[self.iterCount], self.iterCount)
        self.plotPoint(self.loadedData[self.iterCount])
        self.iterCount += 1