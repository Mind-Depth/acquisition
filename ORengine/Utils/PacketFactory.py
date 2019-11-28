from Utils.OreEnum import MessageType
import json

class PacketFactory():

    @staticmethod
    def get_program_state_json(status, message):
        program_state_packet = {
            "message_type": MessageType["PROGRAM_STATE"],
            "status": status,
            "message": message
        }
        return json.dumps(program_state_packet)

    @staticmethod
    def get_fear_event_json(fear, timestamp):
        fear_event_packet = {
            "message_type": MessageType["FEAR_EVENT"],
            "fear_level": fear,
            "timestamp": timestamp
        }
        return json.dumps(fear_event_packet)

    @staticmethod
    def get_json_from_packet(packet):
        return json.loads(packet)