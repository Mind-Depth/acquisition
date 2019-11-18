#!/usr/local/bin/python3

from http.server import BaseHTTPRequestHandler
from io import BytesIO
import json

class MiddlewareHttpHandler(BaseHTTPRequestHandler):
    def send_cors_header(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "*")
        self.send_header("Access-Control-Allow-Headers", "Accept,Content-Type,Origin")

    def do_HEAD(self):           
        self.send_response(200)
        self.send_cors_header()
        self.end_headers()

    def do_OPTIONS(self):           
        self.send_response(200)
        self.send_cors_header()
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.end_headers()

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
            packet = json.loads(body)
            self.server.on_packet_received(packet, self)
        except json.decoder.JSONDecodeError:
            print('ERROR: Unable to parse the current Json : ' + str(body))