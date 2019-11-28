#!/usr/local/bin/python3

import os
import numpy
from numpy import loadtxt
from xgboost import XGBClassifier

class FearEngine():
    DEFAULT_DATASET = os.path.join(os.path.dirname(__file__), '..', 'TrainingDataset', 'ChichNRob.csv')

    def __init__(self, dataset_path=DEFAULT_DATASET):
         self.m_model = XGBClassifier()
         self.m_dataset_path = dataset_path
         self.m_chunck_size = 10
         self.reset()
         
    def train_ia(self):
        print('...Training AI...')
        training_dataset = loadtxt(self.m_dataset_path, delimiter=",")
        X = training_dataset[:,:10]
        Y = training_dataset[:,10]
        self.m_model.fit(X, Y)
        print('...Training completed...')

    def predict_buff(self, buff):
        bpms, timestamps = zip(*buff)
        (_, fear), = self.m_model.predict_proba(numpy.array([bpms]))
        return float(fear)

    def analyse_ai_result(self, buff, callback):
        fear = self.predict_buff(self.m_curr_buff)
        print('AI result : ' + str(fear))
        callback(fear, buff[-1][1])

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