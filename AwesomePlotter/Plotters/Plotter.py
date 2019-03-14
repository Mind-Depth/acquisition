#!/usr/local/bin/python3

from enum import Enum

from PyQt5.QtWidgets import QSizePolicy

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.animation as animation

class PlotterType(Enum):
    READING = 0
    RECORDING = 1

class Plotter(FigureCanvas):
    def __init__(self, parent=None, handler=None, plotterType=PlotterType.READING, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)

        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.handler = handler
        self.plotterType = plotterType
        self.time = 0
        self.rng = 40
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

    def startTimer(self, trueStart=True):
        if trueStart:
            self.timer = self.new_timer(1000, [(self.updateCanvas, (), {})])
        self.timer.start()

    def stopTimer(self, trueStop=True):
        self.timer.stop()
        if trueStop:
            self.time = 0

    def updateCanvas(self):
        if self.handler is not None:
            self.handler.onGraphUpdate([0], self.time)
        self.time += 1

    def plotPoint(self, ax, point, color='blue'):
        self.adaptRange(self.time)
        ax.scatter(self.time, point, c=color)
        self.draw()

    def plotData(self, data, color):
        # TODO // PUT SAME SCALAR HERE >:(
        xPoints = []
        yPoints = []
        i = 0
        for point in data:
            if not isinstance(data[0], list):
                yPoints.append(point)
                xPoints.append(i)
                i += 1
            else:
                xPoints.append(point[1])
                yPoints.append(point[0])
        self.ax.plot(xPoints, yPoints, color)
        self.draw()    

    def plotEvents(self, time, color='blue'):
        self.ax2.scatter(time, [0], c=color)
        self.draw()

    def adaptRange(self, time):
        if self.plotterType is PlotterType.READING:
            if time < self.rng:
                minTime = -(self.rng) + time
            else:
                minTime = time - self.rng
            maxTime = time + self.rng
            self.ax.set_xlim(minTime, maxTime)
            self.ax.set_ylim(40, 150)
            self.ax2.set_xlim(minTime, maxTime)
            self.ax2.set_ylim(-1, 1)
        else:
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