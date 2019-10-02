#!/usr/bin/env python3

import requests
import threading
import json
from Config import Config
from Websockets import Websockets
from NamedPipeManager import NamedPipeManager

import sys

old_write = sys.stdout.write
def _write(*args, **kwargs):
    old_write(*args, **kwargs)
    sys.stdout.flush()
sys.stdout.write = _write

import traceback

class Requestor():

    def get_handler_dict(self):
        return {
            'INIT': self.handle_init,
            'CONTROL_SESSION': self.handle_control_session,
            'FEAR_EVENT': self.handle_fear_event,
            'PROGRAM_STATE': self.handle_program_state,
            'BIOFEEDBACK': self.handle_biofeedback
        }

    def init_message_type(self):
        return {
            'INIT': 'INIT',
            'PROGRAM_STATE': 'PROGRAM_STATE',
            'CONTROL_SESSION': 'CONTROL_SESSION',
            'FEAR_EVENT': 'FEAR_EVENT',
            'BIOFEEDBACK': 'BIOFEEDBACK'
        }

    def __init__(self, socket_callback, config, handler_debug):

       self.m_debug_callback = handler_debug 
       self.m_config = config
       self.m_socket_callback = socket_callback
       self.m_message_type = self.init_message_type()
       self.m_handler_dict = self.get_handler_dict()
       self.m_state_init_android = False
       self.m_state_init_ai = False
       self.m_websocket_manager = Websockets()
    #    self.m_pipe_manager = NamedPipeManager(self.m_config)

    #json_payload => dict object
    def post_wrapper(self, address, json_payload):
        try:
            r = requests.post(address , json=json_payload)
        except:
            print('broke', address, json_payload)
            print(''.join(traceback.format_exception(*sys.exc_info())))
            raise
        print(r, r.content)
        assert r.status_code == 200, (r, r.content)
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
        

    # def start_name_pipe_reader(self, requestor_callback):
    #     t = threading.Thread(target=self.m_pipe_manager._read, args=[requestor_callback])
    #     t.start()

    def start_socket_reader(self, socket_callback):
        t = threading.Thread(target=self.m_websocket_manager._read, args=[socket_callback])
        t.start()

    #
    # Request formating fonction suite
    #

    """handle_init takes route, port and address as kwargs"""
    def handle_init(self, **kwargs):
        print('IN HANDLE INIT')
        try:
            json_payload = {
                'message_type': self.m_message_type['INIT'],
                'client_ip': self.m_config.m_local_ip,
                'client_port': kwargs['port'],
                'client_rte': kwargs['route']
            }
            print('INIT PAYLOAD:')
            print(json_payload)
            response = self.post_wrapper(kwargs['address'], json_payload)
            print('Response', response)
            if response['status'] is False:
##                if self.m_config.m_ai_address in response['url']:
                if kwargs['address'] == 'http://localhost:4242':
                    self.start_request('CONTROL_SESSION', address=self.m_config.m_android_address, status=False)
                    # self.send_error_by_named_pipe(response['data']['message'])
                else:
                    self.start_request('CONTROL_SESSION', address=self.m_config.m_ai_address, status=False)
                    # self.send_error_by_named_pipe(response['data']['message'])
            else:
##                if self.m_config.m_ai_address in response['url']:
                if kwargs['address'] == 'http://localhost:4242':
                    print('AI Ready')
                    self.m_state_init_ai = True
                else:
                    print('Android Ready')
                    self.m_state_init_android = True

                if self.m_state_init_android is True and self.m_state_init_ai is True:
                    print('State are True')
                    try:
                        status = self.m_websocket_manager._connect(self.m_config.m_socket_host, self.m_config.m_socket_port)
                        t = threading.Thread(target=self.m_websocket_manager._read, args=[self.m_socket_callback])
                        t.start()
                    except:
                        print('Except')
                        return {'status': False, "message": "socket connexion failed"}

                    print('Connect', self.m_config.m_socket_host, self.m_config.m_socket_port)
#                    status = self.m_websocket_manager._connect(self.m_config.m_socket_host, self.m_config.m_socket_port)
                    if status == False:
                        print('Status False')
                        self.start_request('CONTROL_SESSION', address=self.m_config.m_android_address, status=False)
                        self.start_request('CONTROL_SESSION', address=self.m_config.m_ai_address, status=False)
                        # self.send_error_by_named_pipe('Cannot establish network connexion with ORE')
                        return False

                    self.start_socket_reader(self.m_socket_callback)
                    print('Send to generation')
                    print('SET UP AND READY')
                    self.m_debug_callback()
                    # self.m_pipe_manager._write({'message_type': 'PROGRAM_STATE', 'status': True, 'message': 'Set-up and ready'})
        except:
            import sys
            import traceback
            print('Mechant Sifi Requestor.py')
            print(''.join(traceback.format_exception(*sys.exc_info())))
            pass #TODO handle post error

    """handle_control_session takes status and address as kwargs"""
    def handle_control_session(self, **kwargs):
        print('handle_control_session [ENTER]', kwargs)
        try:
            json_payload = {
                'message_type': self.m_message_type['CONTROL_SESSION'],
                'status': kwargs['status']
            }
            response = self.post_wrapper(kwargs['address'], json_payload)
            print('handle_control_session [SEND]', response)
            if response['status']!= True and kwargs['stop'] == False: #TODO check que c'est bien du Pascal case
                if self.m_config.m_ai_address == kwargs['address']:
                    self.start_request('CONTROL_SESSION', address=self.m_config.m_android_address, status=False, stop=True)
                    # self.m_pipe_manager._write({'message_type': 'PROGRAM_STATE', 'status': False, 'message': response['data']['message']})
                else:
                    self.start_request('CONTROL_SESSION', address=self.m_config.m_ai_address, status=False, stop=True)
                    # self.m_pipe_manager._write({'message_type': 'PROGRAM_STATE', 'status': False, 'message': response['data']['message']})
##            else:
##                #TODO il recoit 2 running en l'etat et c'est nul
##                self.m_pipe_manager._write({'message_type': 'PROGRAM_STATE', 'status': True, 'message': 'Running'})
        except:
            import sys
            import traceback
            print('handle_control_session SSSSSSSSSSSIIIIIIIIIIIIIIIIIFFFFFFFFFFFFFFFFFFFIIIIIIIIIIIIIIII!!!!!!!!!!')
            print(''.join(traceback.format_exception(*sys.exc_info())))
            pass

    """handle_fear_event takes data """
    def handle_fear_event(self, **kwargs):
        print('in handle_fear_event')
        try:
            self.m_pipe_manager._write(kwargs['data'])
        except:
            print('error in handle_fear_event')

    """
        handle_init takes status, message and address as kwargs
        should not be used
    """
    def handle_program_state(self, **kwargs):
        print('handle_program_state ???')
        try:
            json_payload = {
                'message_type': self.m_message_type['PROGRAM_STATE'],
                'status': kwargs['status'],
                'message': kwargs['message']
            }
            response = self.post_wrapper(kwargs['address'], json_payload)
            print('handle_program_state response', response)
        except:
            import sys
            import traceback
            print('Systemicaca handle_program_state')
            print(''.join(traceback.format_exception(*sys.exc_info())))
            raise

    """handle_init takes biofeedback, timestamp and address as kwargs"""
    def handle_biofeedback(self, **kwargs):
        try:
            json_payload = {
                'message_type': self.m_message_type['BIOFEEDBACK'],
                'bf': kwargs['biofeedback'],
                'timestamp': kwargs['timestamp']
            }
            response = self.post_wrapper(kwargs['address'], json_payload)
        except:
            import sys
            import traceback
            print('La scatocratie handle_biofeedback')
            print(''.join(traceback.format_exception(*sys.exc_info())))
            raise

    # def send_error_by_named_pipe(self, message):
    #     self.m_pipe_manager._write({'message_type': 'PROGRAM_STATE', 'status': False, 'message': message})
