import requests


class StoreJson:
    def __init__(self, json_string):
        self.json_sting = json_string

    def store(self, url='http://localhost:8080/marco27-web/v1/pfs/create'):
        json_string_utf8 = str(self.json_sting).encode("utf-8")
        headers = {'Content-type': 'application/json', 'Accept': '*/*'}
        try:
            response = requests.post(url, data=json_string_utf8, headers=headers)
        except Exception as e:
            print("Error store json:\n %s" % json_string_utf8)
            print(e)

        return json_string_utf8
