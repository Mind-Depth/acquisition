#!/usr/local/bin/python3

import socket
import json
from Utils.OreEnum import MessageType
from Utils.OreConstants import AI_PORT, BUFFER_SIZE
from Utils.EnumUtils import EnumEncoder, as_enum

program_state_packet = {
    "message_type": MessageType.PROGRAM_STATE,
    "status": False,
    "message": "Ca marche pas"
}

class OnionRingEngineServer():
    def __init__(self, port):
        self.m_port = port
        self.m_ip = socket.gethostname()
        self.m_socket = socket.socket()
        self.start_server()

    def start_server(self):
        print('Launching the OREngine Server on ' + str(self.m_ip) + ':' + str(self.m_port) + '...')
        self.m_socket.bind((self.m_ip, self.m_port))
        self.m_socket.listen()
        client_socket, address = self.m_socket.accept()
        print('Connection from: ' + str(address))
        while True:
            data = client_socket.recv(BUFFER_SIZE).decode()
            if not data:
                print('Client ' + str(address) + ' disconnected')
                break
            try:
                jsonPacket = json.loads(data, object_hook=as_enum)
                self.packet_parser(jsonPacket, client_socket)
            except:
                print('ERROR: Unable to parse the current Json : ' + str(data))
                self.send_packet_to_client(client_socket, 'ERROR: Unable to parse the current Json : ' + str(data))
        client_socket.close()
        print('Closing the OREngine Server...')

    def send_packet_to_client(self, client_socket, message):
        client_socket.send(message.encode())

    def packet_parser(self, packet, client_socket):
        if (packet["message_type"] == MessageType.PROGRAM_STATE):
            print('PROGRAM_STATE')
            self.send_packet_to_client(client_socket, 'PROGRAM_STATE')
        elif (packet["message_type"] == MessageType.CONTROL_SESSION):
            print('CONTROL_SESSION')
            self.on_control_session_packet_received(packet, client_socket)
        elif (packet["message_type"] == MessageType.BIOFEEDBACK):
            print('BIOFEEDBACK')
            self.send_packet_to_client(client_socket, 'BIOFEEDBACK')
        else:
            print('ERROR: Unknown message type')
            self.send_packet_to_client(client_socket, 'ERROR: Unknown message type')

    def on_control_session_packet_received(self, packet, client_socket):
        if (packet["status"] == True):
            print('Launching Onion Ring Engine AI')
            self.send_packet_to_client(client_socket, 'Launching Onion Ring Engine AI')
        elif (packet["status"] == False):
            print('Stopping Onion Ring Engine AI')
            self.send_packet_to_client(client_socket, 'Stopping Onion Ring Engine AI')
        else:
            print('ERROR: Unable to parse the control session packet')
            self.send_packet_to_client(client_socket, 'ERROR: Unable to parse the current control_session packet')

if __name__ == '__main__':
        OnionRingEngineServer(AI_PORT)