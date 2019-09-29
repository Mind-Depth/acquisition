#!/usr/local/bin/python3

import sys
import threading
from Utils.PrintUtils import log


class KeyboardController():
    def __init__(self, callback):
        self.m_middleware_callback = callback
        self.m_thread = threading.Thread(target = self.run_keyboard_loop)

    def start(self):
        log(self, 'Starting KeyboardController')
        self.m_thread.start()

    def stop(self):
        log(self, 'Stopping KeyboardController')
        self.m_thread.join()

    def run_keyboard_loop(self):
        for line in sys.stdin:
            self.m_middleware_callback(line.rstrip())