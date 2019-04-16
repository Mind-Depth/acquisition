#!/usr/local/bin/python3

from io import BytesIO
from enum import Enum
from http.server import BaseHTTPRequestHandler

from Utils.OreEnum import MessageType, OreCommandType
from Utils.PacketFactory import PacketFactory

class OreHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        jsonPacket = PacketFactory.get_json_from_packet(body)
        self.packet_parser(jsonPacket)
        """try:
            jsonPacket = PacketFactory.get_json_from_packet(body)
            self.packet_parser(jsonPacket)
        except:
            print('ERROR: Unable to parse the current Json : ' + str(body))
            self.send_complete_response(400, PacketFactory.get_program_state_packet(False, 'Unable to parse the current Json'))"""

    def send_complete_response(self, code, content):
        self.send_response(code)
        self.end_headers()
        response = BytesIO()
        response.write(content.encode())
        self.wfile.write(response.getvalue())

    def packet_parser(self, packet):
        if packet["message_type"] == MessageType['CONTROL_SESSION']:
            self.on_control_session_packet_received(packet)
        elif packet["message_type"] == MessageType['INIT']:
            self.on_init_packet_received(packet)
        elif packet["message_type"] == MessageType['BIOFEEDBACK']:
            self.on_biofeedback_packet_received(packet)
        else:
            print('ERROR: Unknown message_type')
            self.send_complete_response(400, PacketFactory.get_program_state_packet(False, 'Unknown message_type'))

    def on_init_packet_received(self, packet):
        self.server.on_post_reiceived(OreCommandType.INIT, self, packet)

    def on_biofeedback_packet_received(self, packet):
        self.server.on_post_reiceived(OreCommandType.BIOFEEDBACK, self, packet)

    def on_control_session_packet_received(self, packet):
        if packet["status"] == True:
            self.server.on_post_reiceived(OreCommandType.START_AI, self)
        elif packet["status"] == False:
            self.server.on_post_reiceived(OreCommandType.STOP_AI, self)
        else:
            print('ERROR: Unable to parse the control_session packet')
            self.send_complete_response(400, PacketFactory.get_program_state_packet(False, 'Unable to parse the control_session packet'))