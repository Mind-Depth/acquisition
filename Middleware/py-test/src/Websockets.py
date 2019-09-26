#!/usr/bin/env python3

import json

import socket
from Config import Config

import sys
old_write = sys.stdout.write
def _write(*args, **kwargs):
    old_write(*args, **kwargs)
    sys.stdout.flush()
sys.stdout.write = _write

class Websockets:

    def __init__(self):
        self.m_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.m_buff_read_size = 1024

    def _connect(self, host, port):
        try:
            print('Le connect', host, int(port))
            self.m_s.connect((host, int(port)))
        except:
            import sys
            import traceback
            print('Mechant Sifi Webocket.py')
            print(''.join(traceback.format_exception(*sys.exc_info())))
            print('Cannot establish the socket connection with ORengine')
            return False
        
    def _read(self, requestor_callback):
        print('In socket read')
        try:
            while True:
                data = self.m_s.recv(self.m_buff_read_size)
                print('Web socket: ', data)
                requestor_callback(json.loads(data.decode()))
        except:
            import sys
            import traceback
            print('LE READ IL EST KC')
            print(''.join(traceback.format_exception(*sys.exc_info())))
            print('Cannot establish the socket connection with ORengine')
            raise
