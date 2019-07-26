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

class MockerCommandType(Enum):
    START = 0
    STOP = 1
    INIT = 2


class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if type(obj) in PUBLIC_ENUMS.values():
            return {"__enum__": str(obj)}
        return json.JSONEncoder.default(self, obj)

def as_enum(d):
    if "__enum__" in d:
        name, member = d["__enum__"].split(".")
        return getattr(PUBLIC_ENUMS[name], member)
    else:
        return d