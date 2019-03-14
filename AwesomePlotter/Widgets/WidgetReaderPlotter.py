#!/usr/local/bin/python3

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QHBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QDesktopWidget, QAction, QFileDialog
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
import numpy as np 

from Plotters.Plotter import Plotter, PlotterType
from Interfaces.IGraphicalUpdateHandler import IGraphicalUpdateHandler, IGraphicalUpdateHandlerFinalMeta

class WidgetReaderPlotter(QWidget, IGraphicalUpdateHandler, metaclass=IGraphicalUpdateHandlerFinalMeta):
    def __init__(self, handler=None):
        QWidget.__init__(self)

        self.handler = handler
        self.canvas = Plotter(self, handler=self, plotterType=PlotterType.READING)
        graphToolBar = NavigationToolbar(self.canvas, self)
        graphToolBar.setMovable(False)
        dockLayout = QVBoxLayout()
        dockLayout.setMenuBar(graphToolBar)
        self.setLayout(dockLayout)
        self.layout().addWidget(self.canvas)
        self.loadedData = []
        self.loadedEvents = []
        
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

    def plotPoint(self, ax, point):
        self.canvas.plotPoint(ax, point)

    def clearData(self):
        self.canvas.clearData()

    def launchMockPlaying(self):
        self.canvas.startTimer()

    def stopMockPlaying(self):
        self.canvas.stopTimer()
        self.clearData()
    
    def pauseMockPlaying(self):
        self.canvas.stopTimer(trueStop=False)

    def resumeMockPlaying(self):
        self.canvas.startTimer(trueStart=False)

    ### MARK : IGraphicalUpdateHandler callbacks ###

    def onGraphUpdate(self, point, time):
        if self.handler is not None:
            self.handler.onGraphUpdate(self.loadedData[time], time)
        self.plotPoint(self.canvas.ax, self.loadedData[time])
        