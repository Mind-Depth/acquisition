#!/usr/local/bin/python3

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO

from Utils.OreEnum import MessageType
from Utils.OreConstants import AI_PORT, AI_IP
from Utils.EnumUtils import EnumEncoder, as_enum

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        try:
            jsonPacket = json.loads(body, object_hook=as_enum)
            self.packet_parser(jsonPacket)
        except:
            print('ERROR: Unable to parse the current Json : ' + str(body))
            self.send_complete_response(400, self.get_program_state_packet(False, 'Unable to parse the current Json'))

    def send_complete_response(self, code, content):
        self.send_response(code)
        self.end_headers()
        response = BytesIO()
        response.write(content.encode())
        self.wfile.write(response.getvalue())

    def get_program_state_packet(self, status, message):
        program_state_packet = {
            "message_type": MessageType.PROGRAM_STATE,
            "status": status,
            "message": message
        }
        return json.dumps(program_state_packet, cls=EnumEncoder)

    def get_fear_event_packet(self, status, fear_accuracy, timestamp):
        fear_event_packet = {
            "message_type": MessageType.FEAR_EVENT,
            "status_fear": status,
            "fear_accuracy": fear_accuracy,
            "timestamp": timestamp
        }
        return json.dumps(fear_event_packet, cls=EnumEncoder)

    def packet_parser(self, packet):
        if (packet["message_type"] == MessageType.CONTROL_SESSION):
            self.on_control_session_packet_received(packet)
        elif (packet["message_type"] == MessageType.BIOFEEDBACK):
            print('BIOFEEDBACK')
        else:
            print('ERROR: Unknown message_type')
            self.send_complete_response(400, self.get_program_state_packet(False, 'Unknown message_type'))

    def on_control_session_packet_received(self, packet):
        if (packet["status"] == True):
            print('Launching Onion Ring Engine AI')
            self.send_complete_response(200, self.get_program_state_packet(True, 'Launching Onion Ring Engine AI'))
        elif (packet["status"] == False):
            print('Stopping Onion Ring Engine AI')
            self.send_complete_response(200, self.get_program_state_packet(True, 'Stopping Onion Ring Engine AI'))
        else:
            print('ERROR: Unable to parse the control_session packet')
            self.send_complete_response(400, self.get_program_state_packet(False, 'Unable to parse the control_session packet'))

class OnionRingEngineHTTPServer():
    def __init__(self, ip, port):
        self.m_ip = ip
        self.m_port = port
        self.m_httpd = HTTPServer((self.m_ip, self.m_port), SimpleHTTPRequestHandler)
        self.start_server()

    def start_server(self):
        print('Launching HTTP server on ' + str(self.m_ip) + ':' + str(self.m_port))
        self.m_httpd.serve_forever()

if __name__ == "__main__":
    OnionRingEngineHTTPServer(AI_IP, AI_PORT)