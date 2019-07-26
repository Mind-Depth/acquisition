#!/usr/local/bin/python3

from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
import json
import threading
from io import BytesIO

from AwesomeHTTPSender import AwesomeHTTPSender
from Utils.PacketFactory import PacketFactory

class AwesomeHttpRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        self.request_callbacks = {
            "PROGRAM_STATE": self.on_program_state_packet_received,
            "BIOFEEDBACK": self.onHReqReceived
        }

        super().__init__(*args, directory="Harvester/", **kwargs)

    def do_OPTIONS(self):           
        self.send_response(200)
        self.send_cors_header()
        self.end_headers()
    
    def send_cors_header(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "*")
        self.send_header("Access-Control-Allow-Headers", "Accept,Content-Type,Origin")

    def send_complete_response(self, code, content):
        self.send_response(code)
        self.send_cors_header()
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = BytesIO()
        response.write(content.encode())
        self.wfile.write(response.getvalue())
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        try:
            jsonPacket = PacketFactory.get_json_from_packet(body)
            self.request_callbacks[jsonPacket["message_type"]](jsonPacket)
        except json.decoder.JSONDecodeError:
            print('ERROR: Unable to parse the current Json : ' + str(body))
            self.send_complete_response(400, PacketFactory.get_program_state_json(False, 'Unable to parse the current Json'))

    def on_program_state_packet_received(self, packet):
        self.server.on_program_state_packet_received(packet)

    def on_biofeedback_packet_received(self, packet):
        self.server.on_biofeedback_packet_received(packet)

class AwesomeHttpServer(HTTPServer):
    def __init__(self, ip, port, android_ip, android_port, biofeedback_callback):
        self.m_ip = ip
        self.m_port = port
        self.m_android_ip = android_ip
        self.m_android_port = android_port
        self.m_callback = biofeedback_callback

        HTTPServer.__init__(self, (self.m_ip, self.m_port), AwesomeHttpRequestHandler)
        self.server_thread = threading.Thread(target=self.serve_forever)
        self.server_thread.daemon = True


    def start(self):
        self.server_thread.start()
        AwesomeHTTPSender.post_data_to_endpoint(self.m_android_ip, self.m_android_port, '/', PacketFactory.get_init_json(self.m_ip, self.m_port, "/"), self.on_positive_init_response_received)

    def stop(self):
        self.shutdown()
        AwesomeHTTPSender.post_data_to_endpoint(self.m_android_ip, self.m_android_port, '/', PacketFactory.get_control_session_json(False), self.on_positive_control_session_response_received)

    def on_positive_init_response_received(self):
        print("on_positive_init_response_received")
        AwesomeHTTPSender.post_data_to_endpoint(self.m_android_ip, self.m_android_port, '/', PacketFactory.get_control_session_json(True), self.on_positive_control_session_response_received)

    def on_positive_control_session_response_received(self):
        print("on_positive_control_session_response_received")

    def on_biofeedback_packet_received(self, packet):
        self.m_callback(packet["bf"], packet["timestamp"])