#!/usr/local/bin/python3

from PyQt5.QtWidgets import QSizePolicy

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.animation as animation

class Plotter(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.rng = 40
        self.initUI()

    def initUI(self):
        self.ax = self.figure.add_subplot(111)
        self.initAxesLabels()

    def initAxesLabels(self):
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('BPM')

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

    def plotPoint(self, point, time, color='blue'):
        self.adaptRange(time)
        self.ax.scatter(time, point, c=color)
        self.draw()

    def adaptRange(self, time):
        if time < self.rng:
            minTime = -(self.rng) + time
        else:
            minTime = time - self.rng
        maxTime = time + self.rng
        self.ax.set_xlim(minTime, maxTime)
        self.ax.set_ylim(40, 150)

    def clearData(self):
        self.ax.clear()
        self.initAxesLabels()
        self.draw()