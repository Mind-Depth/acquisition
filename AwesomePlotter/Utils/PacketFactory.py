from Utils.EnumUtils import MessageType
import json

class PacketFactory():

    @staticmethod
    def get_init_json(ip, port, rte):
        program_state_packet = {
            "message_type": MessageType["INIT"],
            "client_ip": ip,
            "client_port": port,
            "client_rte": rte
        }
        return json.dumps(program_state_packet)
        
    @staticmethod
    def get_program_state_json(status, message):
        program_state_packet = {
            "message_type": MessageType["PROGRAM_STATE"],
            "status": status,
            "message": message
        }
        return json.dumps(program_state_packet)

    @staticmethod
    def get_control_session_json(status):
        fear_event_packet = {
            "message_type": MessageType["CONTROL_SESSION"],
            "status": status,
        }
        return json.dumps(fear_event_packet)

    @staticmethod
    def get_json_from_packet(packet):
        return json.loads(packet)