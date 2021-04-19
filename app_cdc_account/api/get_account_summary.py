# url = https://api.crypto.com/v2/private/get-account-summary

import hashlib
import hmac
import time

import requests


class GetAccountSummary:
    def __init__(self, url, api_key, secret_key):
        self.url = url
        self.api_key = api_key
        self.secret_key = secret_key

    def do_post(self, request_id, currency):

        req = {
            "id": request_id,
            "method": "private/get-account-summary",
            "api_key":  self.api_key,
            "params": {
                "currency": currency,
            },
            "nonce": int(time.time() * 1000)
        }

        try:
            # First ensure the params are alphabetically sorted by key
            param__string = ""

            if "params" in req:
                for key in sorted(req['params']):
                    param__string += key
                    param__string += str(req['params'][key])

            sig_pay_load = req['method'] + str(req['id']) + req['api_key'] + param__string + str(req['nonce'])

            req['sig'] = hmac.new(
                bytes(str(self.secret_key), 'utf-8'),
                msg=bytes(sig_pay_load, 'utf-8'),
                digestmod=hashlib.sha256
            ).hexdigest()

            response = requests.post(self.url, data=req)

        except Exception as e:
            print("Error GetAccountSummary:\n %s" % req)
            print(e)

        return response
