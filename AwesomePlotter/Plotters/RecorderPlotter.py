#!/usr/local/bin/python3

from PyQt5.QtWidgets import QSizePolicy

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.animation as animation

class RecorderPlotter(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.rng = 40
        self.time = 0
        self.initUI()

    def initUI(self):
        self.ax = self.figure.add_subplot(211)
        self.ax2 = self.figure.add_subplot(212)
        self.initAxesLabel(self.ax, yLabel='BPM')
        self.initAxesLabel(self.ax2, xLabel='Time')
        self.ax.xaxis.set_visible(False)
        self.ax2.yaxis.set_visible(False)

    def initAxesLabel(self, ax, xLabel=None, yLabel=None):
        ax.set_xlabel(xLabel)
        ax.set_ylabel(yLabel)

    def startTimer(self):
        self.timer = self.new_timer(1000, [(self.updateCanvas, (), {})])
        self.timer.start()
    
    def stopTimer(self):
        self.timer.stop()
        self.time = 0

    def updateCanvas(self):
        self.time += 1

    def plotPoint(self, ax, point, time, color='blue'):
        self.adaptRange(time)
        ax.scatter(time, point, c=color)
        self.draw()

    def adaptRange(self, time):
        maxTime = time + self.rng

        self.ax.set_ylim(40, 150)
        self.ax.set_xlim(0, maxTime)
        self.ax2.set_ylim(-1, 1)
        self.ax2.set_xlim(0, maxTime)

    def getTime(self):
        return self.time

    def clearData(self):
        self.ax.clear()
        self.ax2.clear()
        self.initAxesLabel(self.ax, yLabel='BPM')
        self.initAxesLabel(self.ax2, xLabel='Time')
        self.draw()

    
