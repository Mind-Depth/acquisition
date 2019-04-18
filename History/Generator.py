#!/usr/bin/python2
# vim: set fileencoding=utf-8 :

import sys
from os import system
import random

iteration_number = 131
target = ""
random.seed(None)

fear_range = [120, 140]

def start_writing(target):
    i = 0
    current_row = []
    current_bpm = random.randrange(70 ,89, 3)

    with open(target, 'w+') as wfile:

        while i < iteration_number:
            y = 0
            current_row[:] = [0] * 10
            while y != 10:

                if (i >= 30 and i <= 40) or (i >= 80 and i <= 90) or (i >= 110 and i <= 120):
                    if current_bpm < 90:
                        current_bpm += 50
                    while current_row[y] < 120 or current_row[y] > 140:
                        current_row[y] = (random.randrange(current_bpm - 2, current_bpm + 2, 3))
                    current_bpm = current_row[y]
                else:
                    if current_bpm > 90:
                        current_bpm -= 50
                    while current_row[y] < 70 or current_row[y] > 89:
                        current_row[y] = (random.randrange(current_bpm - 2, current_bpm + 2, 3))
                    current_bpm = current_row[y]
                y += 1

            tmp = str(current_row)[1:-1] + '\n'
            wfile.write(tmp)
            i += 1

try:
    target = sys.argv[1]
    start_writing(target)
except OSError as e:
    print(e)