#!/usr/local/bin/python3

from enum import Enum
import json

class MessageType(Enum):
    PROGRAM_STATE = 0
    FEAR_EVENT = 1
    CONTROL_SESSION = 2
    BIOFEEDBACK = 3

