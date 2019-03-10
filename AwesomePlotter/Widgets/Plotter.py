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
        self.initUI()

    def initUI(self):
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('BPM')

    def plotData(self, data):
        self.ax.plot(data, 'b-')
        self.draw()    

    def plotPoint(self, point, time):
        rng = 20
        if time < rng:
            minTime = -rng + 1
        else:
            minTime = time - rng
        maxTime = time + rng
        self.ax.set_xlim(minTime, maxTime)
        self.ax.set_ylim(40, 150)

        self.ax.scatter(time, point, c='blue')

        self.draw()

    def clearData(self):
        self.ax.clear()
        self.draw()