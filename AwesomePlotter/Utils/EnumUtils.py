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

PUBLIC_ENUMS = {
    'MessageType': MessageType
}