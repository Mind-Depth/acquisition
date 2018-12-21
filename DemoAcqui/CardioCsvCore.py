#!/usr/local/bin/python3
import time
import numpy
from numpy import loadtxt
from numpy import matrix
from FearClassifier import fear_classifier

def load_csv():
    dataset = loadtxt('fakeDS.csv', delimiter=",")
    return dataset

def main():
    fc = fear_classifier()
    fc.train_ia()
    dataset = load_csv()

    for dataBuff in dataset:
        buff = numpy.ndarray(shape=(2,10), dtype=int)
        buff[0] = dataBuff
        buff[1] = [0,0,0,0,0,0,0,0,0,0]
        for data in dataBuff:
            print(data)
            time.sleep(0.5)
        fc.predict_buff(buff)
    

if __name__ == "__main__":
    main()