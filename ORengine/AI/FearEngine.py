#!/usr/local/bin/python3

import os
import abc

from enum import Enum
from numpy import loadtxt
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from Utils.OreEnum import FearEngineState

class FearEngine():
    DEFAULT_DATASET = os.path.join(os.path.dirname(__file__), '..', 'TrainingDataset', 'defaultDataset.csv')

    def __init__(self, dataset_path=DEFAULT_DATASET):
         self.m_model = XGBClassifier()
         self.m_dataset_path = dataset_path
         self.m_chunck_size = 10
         self.reset()
         
    def train_ia(self):
        print('...Training AI...')
        training_dataset = loadtxt(self.m_dataset_path, delimiter=",")

        # split data into X and y
        X = training_dataset[:,0:10]
        Y = training_dataset[:,10]

        seed = 7
        test_size = 0.33
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_size, random_state=seed)
    
        # fit m_model no training data
        self.m_model.fit(X_train, Y_train)
        
        print('...Training completed...')

    def predict_buff(self, buff):
        analysed_buff = []
        for bf in buff:
            analysed_buff.append(bf[0])
        y_pred = self.m_model.predict(analysed_buff)
        predictions = [round(value) for value in y_pred]
        accuracy = accuracy_score(y_pred, predictions)
        
        if (predictions[0] == 0):
            return False, accuracy
        else:
            return True, accuracy

    def analyse_ai_result(self, buff, callback):
        result, accuracy = self.predict_buff(self.m_curr_buff)
        print('AI result : ' + str(result))
        if result:
            if self.m_state is FearEngineState.IDLE:
                print('Start of a new fear segment')
                self.m_state = FearEngineState.AFRAID
                callback(result, accuracy, buff[0][1])
        else:
            if self.m_state is FearEngineState.AFRAID:
                print('End of the current fear segment')
                self.m_state = FearEngineState.IDLE
                callback(result, accuracy, buff[self.m_chunck_size - 1][1])

    def add_bf(self, bf, time, callback):
        if len(self.m_curr_buff) < self.m_chunck_size:
            self.m_curr_buff.append([bf, time])
            print('Adding following bf: ' + str(bf) + ' captured at : ' + str(time))
            print('Current buffer (INIT MODE) : ' + str(self.m_curr_buff) + ' size = ' + str(len(self.m_curr_buff)))
            if len(self.m_curr_buff) == self.m_chunck_size:
                print('Launching buff analysis...')
                self.analyse_ai_result(self.m_curr_buff, callback)
        else:
            elem_rm = self.m_curr_buff.pop(0)
            self.m_curr_buff.append([bf, time])
            print('Adding following bf: ' + str(bf) + ' captured at : ' + str(time))
            print('Removing following bf : ' + str(elem_rm[0]) + ' captured at : ' + str(elem_rm[1]))
            print('Launching buff analysis...')
            self.analyse_ai_result(self.m_curr_buff, callback)
            
    def reset(self):
        self.m_curr_buff = []
        self.m_state = FearEngineState.IDLE