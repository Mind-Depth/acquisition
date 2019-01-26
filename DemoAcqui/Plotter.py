#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

class Plotter:
    regSpan = []
    fearSpan = []
    keep = True

    def __init__(self):
        plt.xlabel('Time')
        plt.ylabel('Beats per minute')
        #plt.axis([0, 20, 50, 150])

    def startPrint(self):
        #count = 0
        while(Plotter.keep):
            self.printPlot(np.random.random())
            limits = plt.xlim()
            if (limits[1] - limits[0] > 19):
                plt.xlim(limits[0] + 1, limits[1] + 1)
            plt.xlim()
            plt.plot(Plotter.regSpan, 'b')
            plt.plot(Plotter.fearSpan, 'r')
            plt.pause(0.05)
            #count += 1
            #if (count % 5 == 0):
            #    self.printBuff([np.random.random() for i in range(5)], True if np.random.random() < 0.5 else False)
            #if (count == 40):
            #    stopPrint()
        plt.show()

    def printPlot(self, dot):
        Plotter.regSpan.append(dot)

    def printBuff(self, buffer, isFear):
        if (not isFear):
            Plotter.fearSpan.extend([np.nan for i in range(10)])
        else:
            Plotter.fearSpan.extend(buffer)

    def stopPrint(self):
        Plotter.keep = False

import threading
import sched, time

def threadedFunction(plotterClass):
    toto = 0
    while (1):
        print(toto)
        toto += 1

def main():
    plotter = Plotter() #init my class, loop not started yet
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(0.1, 1, threadedFunction, kwargs={'plotterClass': plotter}) #replace threadedFunction by the CSV stuff, pass the parameters with the following arguments
    threading.Timer(0, scheduler.run).start()
    plotter.startPrint() #start the loop

if __name__ == "__main__":
    main()