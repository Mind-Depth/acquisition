#!/usr/local/bin/python3

from Utils.PrintUtils import log
import threading
import requests
import json

class MiddlewareHttpController():
    def  __init__(self, callbacks):
        self.m_callbacks = callbacks

    def post_data_to_endpoint(self, data, url):
        new_thread = threading.Thread(target = self.post, args = (data, url))
        new_thread.start()

    def get_header(self):
        return {
            'Content-Type': 'application/json'
        }

    def compute_response(self, data, resp, url):
        if data["message_type"] is "INIT":
            self.m_callbacks["INIT"](resp, url)
        elif data["message_type"] is "CONTROL_SESSION":
            self.m_callbacks["CONTROL_SESSION"](resp, url)

    def post(self, data, url):
        try:
            log(self, 'Sending {} to {}'.format(data, url))
            session = requests.Session()
            session.trust_env = False
            response = session.post(url = url, headers = self.get_header(), data = json.dumps(data), timeout=5)
            json_resp = response.json()
            resp_url = response.url
            response.close()

            log(self, 'Response {} received from {}'.format(json_resp, resp_url))
            self.compute_response(data, json_resp, resp_url)
        except Exception as e:
            log(self, '{} {} {}'.format(url, data, e))
            self.compute_response(data, dict(status=False), url)
            raise
