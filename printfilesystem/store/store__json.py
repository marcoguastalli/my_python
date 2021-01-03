import requests


class StoreJson:
    def __init__(self, json_model):
        self.json_model = json_model

    def store(self, url='http://localhost:8080/marco27-web/v1/pfs/create'):
        json_as_sting = str(self.json_model).encode("utf-8")
        headers = {'Content-type': 'application/json', 'Accept': '*/*'}
        try:
            response = requests.post(url, data=json_as_sting, headers=headers)
        except Exception as e:
            print("Error store json:\n %s" % json_as_sting)
            print(e)

        result = json_as_sting
        return result
