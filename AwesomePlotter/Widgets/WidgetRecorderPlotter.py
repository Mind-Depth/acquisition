#!/usr/local/bin/python3

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QHBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QDesktopWidget, QAction, QFileDialog
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
import numpy as np 

from Plotters.Plotter import Plotter, PlotterType

class WidgetRecorderPlotter(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.canvas = Plotter(parent=self, plotterType=PlotterType.RECORDING)
        graphToolBar = NavigationToolbar(self.canvas, self)
        graphToolBar.setMovable(False)
        dockLayout = QVBoxLayout()
        dockLayout.setMenuBar(graphToolBar)
        self.setLayout(dockLayout)
        self.layout().addWidget(self.canvas)
        self.firstLaunch = True

    def logEvent(self):
        self.canvas.plotPoint(self.canvas.ax2, [0])

    def logBiofeedback(self, bf):
        self.canvas.plotPoint(self.canvas.ax, bf)

    def startRecording(self):
        if self.firstLaunch:
            self.canvas.startTimer()
            self.firstLaunch = False
        else:
            self.canvas.startTimer(trueStart=False)

    def stopRecording(self):
        self.canvas.stopTimer(trueStop=False)

    def clearRecording(self):
        self.canvas.clearData()
        self.firstLaunch = True

    def getActualTime(self):
        return self.canvas.getTime()

    