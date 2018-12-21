#!/usr/bin/python2
# vim: set fileencoding=utf-8 :

import csv
import copy
import sys
from os import system
import random

iteration_number = 131
fname = "base.csv"
target = ""
random.seed(None)

fear_range = [120, 140]

def start_writing(fname, fieldnames, target):
    i = 0
    current_row = {'bpm': 0}
    current_bpm = random.randrange(70 ,89, 3)

    with open(target, 'a+') as wfile:
        writer = csv.DictWriter(wfile, fieldnames)

        while i < iteration_number:
            
            current_row['bpm'] = 0

            if (i >= 30 and i <= 40) or (i >= 80 and i <= 90) or (i >= 110 and i <= 120):
                if current_bpm < 90:
                    current_bpm += 50
                while current_row['bpm'] < 120 or current_row['bpm'] > 140:
                    current_row['bpm'] = random.randrange(current_bpm - 2, current_bpm + 2, 3)
                current_bpm = current_row['bpm']
            else:
                if current_bpm > 90:
                    current_bpm -= 50
                while current_row['bpm'] < 70 or current_row['bpm'] > 89:
                    current_row['bpm'] = random.randrange(current_bpm - 2, current_bpm + 2, 3)
                current_bpm = current_row['bpm']

            writer.writerow(current_row)
            i += 1

try:
    target = sys.argv[1]
    system('cp ' + fname + ' ' + target)
    with open(fname, "rb") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        start_writing(fname, fieldnames, target)
except OSError as e:
    print(e)
finally:
    if len(sys.argv) > 2 and sys.argv[2] == 'crlf':
        exit(0)
    isFirst = True
    new_lines = []
    with open( sys.argv[1], "r") as f:
        lines = f.readlines()
        for x in lines:
            new_lines.append(x[:-2])
        with open('final.csv', 'w+') as final:
            for x in new_lines:
                if isFirst is True:
                    x += 'm'
                    isFirst = False
                x += '\n'
                final.write(x)