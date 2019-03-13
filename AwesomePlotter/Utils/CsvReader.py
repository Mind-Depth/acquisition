#!/usr/local/bin/python3

from numpy import loadtxt

class CsvReader():
    def __init__(self, filepath):
        self.filepath = filepath
        self.dataset = self.loadCsv()

    def loadCsv(self):
        dataset = loadtxt(self.filepath, delimiter=",")
        return dataset
    
    def getData(self):
        return self.dataset