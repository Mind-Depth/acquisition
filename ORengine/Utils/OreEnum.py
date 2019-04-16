#!/usr/local/bin/python3

from enum import Enum
import json

MessageType = {
    "PROGRAM_STATE": "PROGRAM_STATE",
    "FEAR_EVENT": "FEAR_EVENT",
    "CONTROL_SESSION": "CONTROL_SESSION",
    "BIOFEEDBACK": "BIOFEEDBACK",
    "INIT": "INIT"
}

class OreCommandType(Enum):
    START_AI = 0
    STOP_AI = 1
    BIOFEEDBACK = 2

class FearEngineState(Enum):
    IDLE = 0
    AFRAID = 1