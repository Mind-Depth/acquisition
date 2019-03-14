#!/usr/local/bin/python3

import os
from Utils.CsvUtils import writeCsv

class SessionRecorderController():
    def __init__(self, sessionName):
        self.sessionName = sessionName
        self.biofeedbacks = []
        self.events = []
        self.sessionNbr = 0
        self.mainFolder = './Sessions/' + self.sessionName + '/'

    def createEnv(self):
        if not os.path.isdir(self.mainFolder):
            os.makedirs(self.mainFolder)
    
    def addEvent(self, event):
        if event not in self.events:
            self.events.append(event)
    
    def addBiofeedback(self, bfb):
        if bfb not in self.biofeedbacks:
            self.biofeedbacks.append(bfb)

    def flushData(self):
        self.biofeedbacks.clear()
        self.events.clear()

    def saveData(self):
        if len(self.events) == 0 and len(self.biofeedbacks) == 0:
            return
        for i in range(0, 1000):
            if not os.path.isdir(self.mainFolder + str(i)):
                self.sessionNbr = i
                break
        os.mkdir(self.mainFolder + str(self.sessionNbr))
        bioFile = self.mainFolder + str(self.sessionNbr) + '/bio.csv'
        evFile = self.mainFolder + str(self.sessionNbr) + '/ev.csv'
        writeCsv(bioFile, self.biofeedbacks)
        writeCsv(evFile, self.events)
        print('Files ' + bioFile + ' and ' + evFile + ' have been successfully created...')