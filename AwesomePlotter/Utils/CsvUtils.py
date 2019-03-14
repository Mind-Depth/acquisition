#!/usr/local/bin/python3

import os
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

def getCsvFilesFromFolder(folderPath):
    csvList = []
    fileList = os.listdir(folderPath)
    for f in fileList:
        if str.__contains__(f, '.csv'):
            csvList.append(folderPath + '/' + f)
    return csvList