#!/usr/local/bin/python3

import unittest
import numpy
from numpy import loadtxt

class TestTrainingDataConsistency(unittest.TestCase):

    def load_csv(self):
        dataset = loadtxt('../TrainingDataset/defautlDataset.csv', delimiter=",")
        return dataset
        
    def test_minimum_row_amount_relevance(self):
        dataFile = self.load_csv()
        self.assertGreaterEqual(len(dataFile), 500)

    def test_global_content(self):
        dataFile = self.load_csv()
        for dataBuf in dataFile:
            self.assertEqual(dataBuf.size, 11)

    def test_data_consistency(self):
        dataFile = self.load_csv()
        for dataBuf in dataFile:
            i = 0
            for data in dataBuf:
                if (i >= 0 and i <= 9):
                    self.assertGreaterEqual(len(str(int(data))), 2)
                else:
                    self.assertEqual(len(str(int(data))), 1)
                i += 1