import requests

class AwesomeHTTPSender():

    @staticmethod
    def post_data_to_endpoint(ip, port, rte, data, callback=None):
        url = 'http://' + ip + ':' + str(port) + rte
        json = data
        session = requests.Session()
        try:
            response = session.post(url = url, headers=AwesomeHTTPSender.get_header(), data = data, timeout=None)
            if response.status_code == 200:
                callback()
        except requests.exceptions.ReadTimeout: 
            pass

    @staticmethod
    def get_header():
        return {
            'Content-Type': 'application/json'
        }