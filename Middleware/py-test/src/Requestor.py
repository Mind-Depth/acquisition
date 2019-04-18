#!/usr/bin/env python3

import requests
import threading
from Config import Config

class Requestor():

    def get_handler_dict(self):
        return {
            'INIT': self.handle_init,
            'CONTROL_SESSION': self.handle_control_session,
            'FEAR_EVENT': self.handle_fear_event,
            'PROGRAM_STATE': self.handle_program_state,
            'BIOFEEDBACK': self.handle_biofeedback,
        }

    def init_message_type(self):
        return {'INIT': 'INIT', 'PROGRAM_STATE': 'PROGRAM_STATE', 'FEAR_EVENT': 'FEAR_EVENT', 'BIOFEEDBACK': 'BIOFEEDBACK'}

    def __init__(self, config=Config()):
       self.m_config = config
       self.m_message_type = self.init_message_type()
       self.m_handler_dict = self.get_handler_dict()

    #json_payload => dict object
    def post_wrapper(self, address, json_payload):
        r = requests.post(address , json=json_payload)
        if r.status_code != 200:
            pass
        return r.json()

        # {'args': {},
        #  'data': '{"key": "value"}',
        #  'files': {},
        #  'form': {},
        #  'headers': {'Accept': '*/*',
        #              'Accept-Encoding': 'gzip, deflate',
        #              'Connection': 'close',
        #              'Content-Length': '16',
        #              'Content-Type': 'application/json',
        #              'Host': 'httpbin.org',
        #              'User-Agent': 'python-requests/2.4.3 CPython/3.4.0',
        #              'X-Request-Id': 'xx-xx-xx'},
        #  'json': {'key': 'value'},
        #  'origin': 'x.x.x.x',
        #  'url': 'http://httpbin.org/post'}


    def start_request(self, message_type, **kwargs):
        t = threading.Thread(target=self.m_handler_dict[message_type], kwargs=kwargs)
        t.start()
        
    #
    # Request formating fonction suite
    #


    """handle_init takes route and address as kwargs"""
    def handle_init(self, **kwargs):
        try:
            json_payload = {
                'message_type': self.m_message_type['INIT'],
                'client_ip': self.m_config.m_public_ip,
                'client_port': self.m_config.m_port,
                'client_rte': kwargs['route']
            }
            response = self.post_wrapper(kwargs['address'], json_payload)
            print(response)
            if 'program_state' not in response['data']:
               pass # send control_session 
            if self.m_config.m_ai_address in response['url']:
                pass
                
            else:
                pass
                
        except:
            pass #todo handle post error

    """handle_control_session takes status and address as kwargs"""
    def handle_control_session(self, **kwargs):
        try:
            json_payload = {
                'message_type': self.m_message_type['CONTROL_SESSION'],
                'status': kwargs['status']
            }
            response = self.post_wrapper(kwargs['address'], json_payload)
            print(response)
            if kwargs['status'] != response.data['status']:
                if self.m_config.m_ai_address == kwargs['address']:
                    self.start_request('CONTROL_SESSION', address=self.m_config.m_android_address, status=False)
                else:
                    self.start_request('CONTROL_SESSION', address=self.m_config.m_ai_address, status=False)
        except:
            pass

    """handle_fear_event takes status_fear, fear_accuracy, timestamp and address as kwargs"""
    def handle_fear_event(self, **kwargs):
        try:
            json_payload = {
                'message_type': self.m_message_type['FEAR_EVENT'],
                'status_fear': kwargs['status_fear'],
                'fear_accuracy': kwargs['fear_accuracy'],
                'timestamp': kwargs['timestamp']
            }
            response = self.post_wrapper(kwargs['address'], json_payload)
            print(response)
        except:
            pass

    """handle_init takes status, message and address as kwargs"""
    def handle_program_state(self, **kwargs):
        try:
            json_payload = {
                'message_type': self.m_message_type['PROGRAM_STATE'],
                'status': kwargs['status'],
                'message': kwargs['message']
            }
            response = self.post_wrapper(kwargs['address'], json_payload)
            print(response)
        except:
            pass

    """handle_init takes biofeedback, timestamp and address as kwargs"""
    def handle_biofeedback(self, **kwargs):
        try:
            json_payload = {
                'message_type': self.m_message_type['BIOFEEDBACK'],
                'bf': kwargs['biofeedback'],
                'timestamp': kwargs['timestamp']
            }
            response = self.post_wrapper(kwargs['address'], json_payload)
            print(response)
        except:
            pass
