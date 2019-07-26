#!/usr/local/bin/python3

from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
import json

from AwesomeHTTPSender import AwesomeHTTPSender
from Utils.PacketFactory import PacketFactory

class AwesomeHttpRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        self.request_callbacks = {
            "PROGRAM_STATE": self.on_program_state_packet_received,
            "BIOFEEDBACK": self.onHReqReceived
        }

        super().__init__(*args, directory="Harvester/", **kwargs)
    
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
        self.m_android_app_ready = False

        HTTPServer.__init__(self, (self.m_ip, self.m_port), AwesomeHttpRequestHandler)

        AwesomeHTTPSender.post_data_to_endpoint(self.m_android_ip, self.m_android_port, '/', PacketFactory.get_init_json(self.m_ip, self.m_port))
        self.serve_forever()

    def on_biofeedback_packet_received(self, packet):
        print(packet)
        #self.m_callback(packet["bf"], packet["timestamp"])

    def on_program_state_packet_received(self, packet):
        if packet["status"] == True:
            self.m_android_app_ready = True
            AwesomeHTTPSender.post_data_to_endpoint(self.m_android_ip, self.m_android_port, '/', PacketFactory.get_control_session_json(True))

if __name__ == "__main__":
    AwesomeHttpServer('localhost', 4242, '10.15.194.86', 8080, None)