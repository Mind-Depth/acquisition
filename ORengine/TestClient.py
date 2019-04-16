#!/usr/local/bin/python3

import socket
import json
from Utils.OreEnum import MessageType
from Utils.OreConstants import AI_PORT, AI_IP

init_packet = {
    "message_type": MessageType["INIT"],
    "client_ip": "190.262.15.3",
    "client_port": 8080
}

control_packet_true = {
    "message_type": MessageType["CONTROL_SESSION"],
    "status": True
}

control_packet_false = {
    "message_type": MessageType["CONTROL_SESSION"],
    "status": False
}

fear_event_packet = {
    "message_type": MessageType["FEAR_EVENT"],
    "status_fear": True,
    "fear_accuracy": 0.0,
    "timestamp": 1234532
}

program_state_packet = {
    "message_type": MessageType["PROGRAM_STATE"],
    "status": False,
    "message": "Ca marche pas"
}

biofeedback_packet = {
    "message_type": MessageType["BIOFEEDBACK"],
    "bf": 55,
    "timestamps": 14323553
}

if __name__ == '__main__':
    #OnionRingEngineTestClient(AI_IP, AI_PORT)
    json_message = json.dumps(init_packet)
    print(json_message)