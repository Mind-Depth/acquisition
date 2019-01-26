#!/usr/local/bin/python3

from numpy import loadtxt
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class fear_classifier():
    def __init__(self):
         self.model = XGBClassifier()
         
    def train_ia(self):
        print("...Training AI...")
        training_dataset = loadtxt('./TrainingDataset/testfile.csv', delimiter=",")

        # split data into X and y
        X = training_dataset[:,0:10]
        Y = training_dataset[:,10]

        seed = 7
        test_size = 0.33
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_size, random_state=seed)
    
        # fit model no training data
        self.model.fit(X_train, Y_train)
        
        print("...Training completed...")

    def predict_buff(self, buff):
        y_pred = self.model.predict(buff)
        predictions = [round(value) for value in y_pred]
        
        print("res :")
        print(predictions)

        if (predictions[0] == 0):
            return False
        else:
            return True