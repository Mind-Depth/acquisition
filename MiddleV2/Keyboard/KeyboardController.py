#!/usr/local/bin/python3

import sys
import threading
from Utils.PrintUtils import log

class KeyboardController():
    def __init__(self, callbacks):
        self.m_middleware_callbacks = callbacks
        self.m_thread = threading.Thread(target = self.run_keyboard_loop)

    def start(self, abort):
        log(self, 'Starting KeyboardController')
        self.abort = abort
        self.m_thread.start()

    def stop(self):
        log(self, 'Stopping KeyboardController')
        self.m_thread.join()

    def run_keyboard_loop(self):
        self.m_is_running = True
        try:
            while self.m_is_running:
                line = input()
                try:
                    self.m_middleware_callbacks[line.rstrip()]()
                except KeyError:
                    log(self, 'The input {} is not valid'.format(line.rstrip()))
        except:
            pass
        self.m_is_running = False
        log(self, 'Aborting')
        self.abort()
