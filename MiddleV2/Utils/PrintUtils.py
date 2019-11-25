#!/usr/local/bin/python3

import os
import logging

_PATH = os.path.split(__file__)[0]
def _relative_path(*path):
	return os.path.realpath(os.path.join(_PATH, *path))

_log_file = _relative_path('..', '..', 'Logs', 'acquisition.txt')
if os.path.exists(_log_file):
	os.remove(_log_file)
logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler(_log_file), logging.StreamHandler()])

def log(sender, msg):
	logging.getLogger(sender.__class__.__name__).info(msg)