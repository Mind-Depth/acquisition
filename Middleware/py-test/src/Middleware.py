#!/usr/bin/env python3

import os
import sys
import bottle
import time
import threading
from Requestor import Requestor
from Config import Config

old_write = sys.stdout.write
def _write(*args, **kwargs):
    old_write(*args, **kwargs)
    sys.stdout.flush()
sys.stdout.write = _write

class Middleware():

    def get_android_message_dict(self):
        return {
            'PROGRAM_STATE': self.android_program_state,
            'BIOFEEDBACK': self.android_biofeedback,
        }


    def get_ai_message_dict(self):
        return {
            'FEAR_EVENT': self.ai_fear_event,
            'PROGRAM_STATE': self.ai_program_state,
        }

    def __init__(self, pipe_name, s_to_c, c_to_s, host='0.0.0.0', port=8080):
        self.m_host = host
        self.m_port = port
        self.m_app = bottle.Bottle()

        self.m_config = Config(pipe_name=pipe_name, server_to_client=s_to_c, client_to_server=c_to_s)
        self.m_requestor = Requestor(self.handler_socket, self.m_config)

        self.m_ai_message_dict = self.get_ai_message_dict()
        self.m_android_message_dict = self.get_android_message_dict()

        self.m_requestor.start_name_pipe_reader(self.handler_named_pipe)
        self._route()

    def _route(self):
        self.m_app.route('/biofeedback', method="POST", callback=self.handler_android)
        self.m_app.route('/server', method="POST", callback=self.handler_ai)

    def _start(self):
        self.m_app.run(host=self.m_host, port=self.m_port)


    def _stop(self):
        # coder les envoies de requetes + sur le pipe disant qu'on stop le server
        #a trouver mieux
        exit(0)

    #
    # NAMED PIPE HANDLERS
    #

    def handler_named_pipe(self, data):
        time.sleep(1)
        if data is None:
            return
        if data['message_type'] == 'INIT':
            print('STARTING INIT')
            self.m_requestor.start_request('INIT', route=self.m_config.m_android_route, \
                port=self.m_config.m_port, address=self.m_config.m_android_address)
            self.m_requestor.start_request('INIT', route=self.m_config.m_ai_route, \
                 port=self.m_config.m_port, address=self.m_config.m_ai_address)
        elif data['message_type'] == 'CONTROL_SESSION':

            self.m_requestor.start_request('CONTROL_SESSION', stop=False, address=self.m_config.m_android_address, status=data.status)
            self.m_requestor.start_request('CONTROL_SESSION', stop=False, address=self.m_config.m_ai_address, status=data.status)

    def handler_socket(self, data):
        print(data)
        if data is None:
           print('DATA IS NONE IN SOCKET CALLBACK')
           return
##        if 'BIOFEEDBACK' in data:
        self.m_requestor.start_request('FEAR_EVENT', data=data)
    #
    # ANDROID HANDLERS
    #

    def handler_android(self):
        print('WELCOME TO HANDLER ANDROID\n')
        print(bottle.request.json)
        try:
            if 'message_type' in bottle.request.json:
                self.m_android_message_dict[bottle.request.json['message_type']](bottle.request.json)
        except:
            import sys
            import traceback
            print('handler_android / Sifi faut pas except tout et n\'importe quwa :|')
            print(''.join(traceback.format_exception(*sys.exc_info())))
            raise
##            print('ERROR IN HANDLER_ANDROID')

    def android_program_state(self, payload):
        try:
            if payload['status'] != True:
                self.m_requestor.send_error_by_named_pipe(payload['message'])
                self.m_requestor.start_request('CONTROL_SESSION', status=False, address=self.m_config.m_ai_address)
        except Exception as e:
            print(e)

    def android_biofeedback(self, payload):
        try:
            if payload['bf'] != 0:
                self.m_requestor.start_request('BIOFEEDBACK', biofeedback=payload['bf'], timestamp=payload['timestamp'], address=self.m_config.m_ai_address)
        except Exception as e:
            print(e)


    #
    # AI HANDLERS
    #

    def handler_ai(self):
        try:
            if 'message_type' in bottle.request.json:
                self.m_ai_message_type[bottle.request.json['message_type']](bottle.request.json)
        except:
            print('ERROR IN HANDLER_AI')
            # gérer le cas

    def ai_program_state(self, payload):
        # this is web socket handled
        print('in cc')

    def ai_fear_event(self, payload):
        # this is web socket handled
        print('in cc2')

def main():
    if len(sys.argv) < 4:
        print('Si usage sans gen, tu peux mettre 3 args random')
        return 1
    middleware = Middleware(sys.argv[1], sys.argv[2], sys.argv[3])
    middleware._start()

if __name__ == "__main__":
    main()
