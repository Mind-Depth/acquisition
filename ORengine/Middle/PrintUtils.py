#!/usr/local/bin/python3

def log(sender, msg):
    print('{} : {}'.format(sender.__class__.__name__, msg))