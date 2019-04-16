#!/usr/local/bin/python3

import socket
import json
from Utils.OreEnum import MessageType
from Utils.OreConstants import AI_PORT, AI_IP, BUFFER_SIZE

init_packet = {
    "message_type": MessageType["INIT"]
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

class OnionRingEngineTestClient():
    def __init__(self, ip, port):
        self.m_ip = ip
        self.m_port = port
        self.m_client_socket = socket.socket()
        self.connect_client()

    def connect_client(self):
        self.m_client_socket.connect((self.m_ip, self.m_port))
        message = input('-> ')
        while message.strip() != '/quit':
            result = self.parse_command(message.strip())
            if (result):
                response = self.m_client_socket.recv(BUFFER_SIZE).decode()
                print('Response: ' + response)
            message = input('-> ')
        self.m_client_socket.close()

    def parse_command(self, command):
        if (command == '/control-start'):
            json_message = json.dumps(control_packet_true)
            self.m_client_socket.send(json_message.encode())
            return True
        elif (command == '/control-stop'):
            json_message = json.dumps(control_packet_false)
            self.m_client_socket.send(json_message.encode())
            return True
        return False

if __name__ == '__main__':
    #OnionRingEngineTestClient(AI_IP, AI_PORT)
    json_message = json.dumps(init_packet)
    print(json_message)