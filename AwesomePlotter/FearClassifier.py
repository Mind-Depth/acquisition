#!/usr/local/bin/python3

import abc
from numpy import loadtxt
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from Interfaces.IAIBehaviourHandler import IAIBehaviourHandler

class FearClassifier():
    def __init__(self, handler=None, datasetPath='./TrainingDataset/defautlDataset.csv'):
         self.model = XGBClassifier()
         self.datasetPath = datasetPath
         self.currBuff = []
         self.handler = handler
         self.chunckSize = 10
         
    def trainIA(self):
        print("...Training AI...")
        training_dataset = loadtxt(self.datasetPath, delimiter=",")

        # split data into X and y
        X = training_dataset[:,0:10]
        Y = training_dataset[:,10]

        seed = 7
        test_size = 0.33
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_size, random_state=seed)
    
        # fit model no training data
        self.model.fit(X_train, Y_train)
        
        print("...Training completed...")

    def predictBuff(self, buff):
        y_pred = self.model.predict(buff)
        predictions = [round(value) for value in y_pred]
        if (predictions[0] == 0):
            return False
        else:
            return True

    def addPoint(self, point, time):
        self.currBuff.append([point, time])
        if len(self.currBuff) is self.chunckSize:
            aiBuff = []
            for point in self.currBuff:
                aiBuff.append(point[0])
            if self.handler is not None and self.predictBuff(aiBuff) is True:
                self.handler.onIaHasPredicted(self.currBuff)
            self.flushCurrentData()

    def getFearSegments(self, buff):
        segments = []
        curBuff = []
        time = 0
        for point in buff:
            curBuff.append([point, time])
            if len(curBuff) is self.chunckSize:
                aiBuff = []
                for point in curBuff:
                    aiBuff.append(point[0])
                if self.predictBuff(aiBuff):
                    segments.append(curBuff.copy())
                curBuff.clear()
            time += 1
        return segments

    def flushCurrentData(self):
        self.currBuff.clear()
