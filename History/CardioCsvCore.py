#!/usr/local/bin/python3
import time
import numpy
import threading
import sched, time
from numpy import loadtxt
from numpy import matrix

from FearClassifier import fear_classifier
from Plotter import Plotter

def load_csv():
    dataset = loadtxt('dataset.csv', delimiter=",")
    return dataset

def start_simulation(plotter):
    fc = fear_classifier()
    fc.train_ia()
    dataset = load_csv()

    for dataBuff in dataset:
        buff = numpy.ndarray(shape=(2,10), dtype=int)
        buff[0] = dataBuff
        buff[1] = [0,0,0,0,0,0,0,0,0,0]
        for data in dataBuff:
            print(data)
            plotter.printPlot(data)
            time.sleep(0.5)
        plotter.printBuff(dataBuff, fc.predict_buff(buff))

def main():
    plotter = Plotter() #init my class, loop not started yet
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(0.1, 1, start_simulation, kwargs={'plotter': plotter}) #replace threadedFunction by the CSV stuff, pass the parameters with the following arguments
    threading.Timer(0, scheduler.run).start()
    plotter.startPrint() #start the loop
    

if __name__ == "__main__":
    main()