#!/usr/local/bin/python3
import random

def create_dataset():
    file = open('./TrainingDataset/testfile.csv','w')
    for x in range(0, 1000):
        randTurn = random.randint(0, 1)
        if (randTurn):
            for y in range(0, 10):
                randBpm = random.randint(70,89)
                file.write(str(randBpm))
                file.write(',')
            file.write('0\n')
        else:
            for y in range(0, 10):
                randBpm = random.randint(120,139)
                file.write(str(randBpm))
                file.write(',')
            file.write('1\n')
    file.close() 

def main():
    create_dataset()

if __name__ == "__main__":
    main()