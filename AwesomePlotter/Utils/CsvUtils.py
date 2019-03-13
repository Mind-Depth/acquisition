#!/usr/local/bin/python3

from numpy import loadtxt

def loadCsv(filepath):
    dataset = loadtxt(filepath, delimiter=",")
    return dataset

def writeCsv(fileName, buff):
    f = open(fileName, "w+")
    i = 0
    for data in buff: 
        if i == len(buff) - 1:
            f.write(str(data))
        else:
            f.write(str(data) + ',')
        i += 1
    f.close() 
