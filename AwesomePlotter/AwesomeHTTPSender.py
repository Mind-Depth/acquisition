import requests

class AwesomeHTTPSender():

    @staticmethod
    def post_data_to_endpoint(ip, port, rte, data):
        url = 'http://' + ip + ':' + str(port) + rte
        json = data
        try:
            requests.post(url = url, data = data, timeout=None) 
        except requests.exceptions.ReadTimeout: 
            pass