#!/usr/local/bin/python3

from numpy import loadtxt
import time
import threading

class CsvReader():
    def __init__(self, callback):
        self.m_callback = callback
        self.m_is_running = False
        self.m_file = self.loadCsv('./data.csv')
        self.m_file_size = len(self.m_file)
        self.m_cur_idx = 0

    def start(self):
        if self.m_is_running:
            print('CsvReader already launched')
            return False
        else:
            self.m_is_running = True
            self.read_next_point()
            return True

    def stop(self):
        if not self.m_is_running:
            print('CsvReader already stopped')
            return False
        else:
            self.m_is_running = False
            return True

    def read_next_point(self):
        if self.m_is_running:
            self.m_callback(self.m_file[self.m_cur_idx], int(time.time()))
            if self.m_cur_idx < self.m_file_size - 1:
                self.m_cur_idx += 1
            else:
                self.m_cur_idx = 0
            threading.Timer(1, self.read_next_point).start()
            

    def loadCsv(self, filepath):
        content = loadtxt(filepath, delimiter=",")
        return content