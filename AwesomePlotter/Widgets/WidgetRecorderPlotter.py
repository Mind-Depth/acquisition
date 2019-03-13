#!/usr/local/bin/python3

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QHBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QDesktopWidget, QAction, QFileDialog
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
import numpy as np 

from Plotters.RecorderPlotter import RecorderPlotter

class WidgetRecorderPlotter(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.canvas = RecorderPlotter(parent=self)
        graphToolBar = NavigationToolbar(self.canvas, self)
        graphToolBar.setMovable(False)
        dockLayout = QVBoxLayout()
        dockLayout.setMenuBar(graphToolBar)
        self.setLayout(dockLayout)
        self.layout().addWidget(self.canvas)

    def logEvent(self):
        self.canvas.plotPoint(self.canvas.ax2, [0], self.canvas.time)

    def startRecording(self):
        self.canvas.startTimer()

    def stopRecording(self):
        self.canvas.stopTimer()

    def clearRecording(self):
        self.canvas.clearData()

    def getActualTime(self):
        return self.canvas.getTime()

    