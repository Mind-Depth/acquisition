#!/usr/local/bin/python3

from enum import Enum

BUFFER_SIZE = 2048
AI_IP = 'localhost'
AI_PORT = 6666

class message_type(Enum):
    PROGRAM_STATE = 0
    FEAR_EVENT = 1
    CONTROL_SESSION = 2
    BIOFEEDBACK = 3