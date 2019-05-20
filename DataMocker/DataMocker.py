#!/usr/local/bin/python3

from http.server import HTTPServer

import json
from io import BytesIO
from http.server import BaseHTTPRequestHandler
from PacketFactory import PacketFactory
from EnumUtils import MessageType, MockerCommandType

import requests

class OnionRingEngineHTTPSender():

    @staticmethod
    def post_data_to_endpoint(ip, port, rte, data):
        url = 'http://' + ip + ':' + str(port) + rte
        json = data
        try:
            requests.post(url = url, data = data, timeout=0.0000000001) 
        except requests.exceptions.ReadTimeout: 
            pass

class DataMockerHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        try:
            jsonPacket = PacketFactory.get_json_from_packet(body)
            self.packet_parser(jsonPacket)
        except json.decoder.JSONDecodeError:
            print('ERROR: Unable to parse the current Json : ' + str(body))
            self.send_complete_response(400, PacketFactory.get_program_state_json(False, 'Unable to parse the current Json'))

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
        else:
            print('ERROR: Unknown message_type')
            self.send_complete_response(400, PacketFactory.get_program_state_json(False, 'Unknown message_type'))

    def on_init_packet_received(self, packet):
        self.server.on_post_reiceived(MockerCommandType.INIT, self, packet)

    def on_control_session_packet_received(self, packet):
        if packet["status"] == True:
            self.server.on_post_reiceived(MockerCommandType.START, self)
        elif packet["status"] == False:
            self.server.on_post_reiceived(MockerCommandType.STOP, self)
        else:
            print('ERROR: Unable to parse the control_session packet')
            self.send_complete_response(400, PacketFactory.get_program_state_json(False, 'Unable to parse the control_session packet'))

class DataMockerHttpServer(HTTPServer):
    def __init__(self, ip, port, *args, **kwargs):
        self.m_ip = ip
        self.m_port = port
        self.m_is_server_init = False
        
        self.m_middleware_ip = None
        self.m_middleware_port = None
        self.m_middleware_rte = None

        HTTPServer.__init__(self, (self.m_ip, self.m_port), DataMockerHTTPRequestHandler)
        self.start_server()

    def start_server(self):
        print('Launching HTTP server on ' + str(self.m_ip) + ':' + str(self.m_port))
        self.serve_forever()

    def on_init_command_received(self, handler, packet):
        if self.m_is_server_init:
            handler.send_complete_response(400, PacketFactory.get_program_state_json(False, 'DataMocker already init'))
        else:
            self.m_is_server_init = True
            self.m_middleware_ip = packet["client_ip"]
            self.m_middleware_port = packet["client_port"]
            self.m_middleware_rte = packet["client_rte"]
            handler.send_complete_response(200, PacketFactory.get_program_state_json(True, 'DataMocker is ready'))

    def on_start_command_received(self, handler, packet):
        handler.send_complete_response(200, PacketFactory.get_program_state_json(True, 'Launching DataMocker'))
        #if not self.m_fear_engine.launch():
        #    handler.send_complete_response(400, PacketFactory.get_program_state_json(False, 'AI already launched'))
        #else:
        #    handler.send_complete_response(200, PacketFactory.get_program_state_json(True, 'Launching Onion Ring Engine AI'))

    def on_stop_command_received(self, handler, packet):
        handler.send_complete_response(200, PacketFactory.get_program_state_json(True, 'Stopping DataMocker'))
        #if not self.m_fear_engine.stop():
        #    handler.send_complete_response(400, PacketFactory.get_program_state_json(False, 'AI already stopped'))
        #else:
        #    handler.send_complete_response(200, PacketFactory.get_program_state_json(True, 'Stopping Onion Ring Engine AI'))

    # MARK : CsvReader callbacks

    def on_new_entry_received(self, bpm, timestamp):
        OnionRingEngineHTTPSender.post_data_to_endpoint(self.m_middleware_ip, self.m_middleware_port, self.m_middleware_rte, PacketFactory.get_biofeedback_json(bpm, timestamp))

    # MARK : BaseHTTPRequestHandler callbacks

    def on_post_reiceived(self, command, handler, packet=None):
        if command is MockerCommandType.INIT:
            self.on_init_command_received(handler, packet)
        elif not self.m_is_server_init:
            handler.send_complete_response(400, PacketFactory.get_program_state_json(False, 'DataMocker not ready yet'))
        elif command is MockerCommandType.START:
            self.on_start_command_received(handler, packet)
        elif command is MockerCommandType.STOP:
            self.on_stop_command_received(handler, packet)

if __name__ == "__main__":
    DataMockerHttpServer('localhost', 8282)