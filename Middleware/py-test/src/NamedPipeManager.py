#!/usr/bin/env python3

import time
import json
import win32file
import pywintypes
from attrdict import AttrDict
import sys

old_write = sys.stdout.write
def _write(*args, **kwargs):
    old_write(*args, **kwargs)
    sys.stdout.flush
sys.stdout.write = _write

def _wrap(f):
    def func(*a, **k):
        try:
            print(f'Call {f.__name__}')
            r = f(*a, **k)
            print(f'End {f.__name__}')
            return r
        except:
            print(f'Broke {f.__name__}')
            raise
    return func

class NamedPipeManager:

    def __init__(self, config):
        self.m_config = config
        try:
            self.m_handle_in = win32file.CreateFile(r'\\.\pipe\{}_{}'.format(self.m_config.m_pipe_name, self.m_config.m_server_to_client),
                                                win32file.GENERIC_READ, 0, None, win32file.OPEN_EXISTING, 0, None)
            self.m_handle_out = win32file.CreateFile(r'\\.\pipe\{}_{}'.format(self.m_config.m_pipe_name, self.m_config.m_client_to_server),
                                                win32file.GENERIC_WRITE, 0, None, win32file.OPEN_EXISTING, 0, None)
        except pywintypes.error as e:
            if e.args[0] == 2:
                raise ValueError("A pipe is not open")
            elif e.args[0] == 109:
                raise ValueError("Broken pipe")
            else:
                raise ValueError("Unknown")

    #TODO check que le READ est bien bloquant
    @_wrap
    def _read(self, requestor_callback):
        '''Reads a json object'''
        while True:
            print('Reading')
            error, msg = win32file.ReadFile(self.m_handle_in, 64*1024)
            print(error, msg)
            assert not error, error
            s = msg.rstrip(b'\x00').decode()
            print('Recv by namedPipe {} : {}'.format(self.m_config.m_pipe_name, s))
            requestor_callback(None if not s else AttrDict(json.loads(s)))

    def _write(self, msg):
        '''Writes a json object'''
        s = json.dumps(msg)
        win32file.WriteFile(self.m_handle_out, (s + '\r\n').encode())
        print('Send {} : {}'.format(self.m_config.m_pipe_name, s))
