# url = https://api.crypto.com/v2/private/get-account-summary

import json
import time

import requests

from .utils.sign_request import sign_request


class GetAccountSummary:
    def __init__(self, url, api_key, secret_key):
        self.url = url
        self.api_key = api_key
        self.secret_key = secret_key

    def do_post(self):
        try:
            req = {
                "id": 1,
                "method": "private/get-account-summary",
                "api_key": self.api_key,
                "params": {},
                "nonce": int(time.time() * 1000)
            }
            req = sign_request(req, self.api_key, self.secret_key)

            headers = {'Content-type': 'application/json'}
            response = requests.post(self.url, headers=headers, data=json.dumps(req))

        except Exception as e:
            print("Error GetAccountSummary:\n %s" % req)
            print(e)

        return response
