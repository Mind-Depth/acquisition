#!/usr/local/bin/python3

import json

class PacketFactory():

    @staticmethod
    def get_program_state_packet(status, message):
        program_state_packet = {
            "message_type": "PROGRAM_STATE",
            "status": status,
            "message": message
        }
        return program_state_packet

    @staticmethod
    def get_control_session_packet(status):
        control_session_packet = {
            "message_type": "CONTROL_SESSION",
            "status": status
        }
        return control_session_packet

    @staticmethod
    def get_init_packet(client_ip, client_port, client_rte):
        init_packet = {
            "message_type": "INIT",
            "client_ip": client_ip,
            "client_port": client_port,
            "client_rte": client_rte
        }
        return init_packet

    @staticmethod
    def get_json_from_packet(packet):
        return json.loads(packet)