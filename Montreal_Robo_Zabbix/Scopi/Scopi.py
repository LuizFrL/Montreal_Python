import requests, json


class Scopi(object):
    def __init__(self):
        self.access_token = self.__get_access_token()

    @staticmethod
    def __get_access_token():
        data = {
            "grant_type": "client_credentials",
            "client_id": "c17cb528f5a2026b2c68f13cdc35d7b08236f0ed01603ba2e6ef2c6f830ce681",
            "client_secret": "dc73a891f45087267d1b958a77d5e5de25bb1151d22c96c5fb115ab16942f801"
        }
        return requests.post('https://api.scopi.com.br/api/oauth/token',
                             data=json.dumps(data), headers={'Content-type': 'application/json'}).json()['access_token']

    def get_indicadores(self):
        url = f'https://api.scopi.com.br/api/v3/indicators?access_token={self.access_token}&active=true'
        indicadores = requests.get(url).json()
        return indicadores

    def put_lines_indicadores(self, id: int, serie, line: int, percentage):
        url = f'https://api.scopi.com.br/api/v3/indicators/{id}'
        data = {
            "access_token": self.access_token,
            "serie": serie,
            "line": line,
            "value": percentage
        }
        return requests.put(url, data=json.dumps(data), headers={'Content-type': 'application/json'})



if __name__ == '__main__':
    b = Scopi()
    for item in b.get_indicadores():
        print(item['name'])