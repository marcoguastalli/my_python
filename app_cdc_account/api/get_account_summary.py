import hashlib
import hmac
import time

API_KEY = "API_KEY"
SECRET_KEY = "SECRET_KEY"


class GetAccountSummary:
    def __init__(self, url):
        self.url = url

    @staticmethod
    def do_post():

        req = {
            "id": 27,
            "method": "private/get-account-summary",
            "api_key": API_KEY,
            "params": {
                "currency": "CRO",
            },
            "nonce": int(time.time() * 1000)
        };

        json_string_utf8 = req

        try:
            # First ensure the params are alphabetically sorted by key
            param__string = ""

            if "params" in req:
                for key in sorted(req['params']):
                    param__string += key
                    param__string += str(req['params'][key])

            sig_pay_load = req['method'] + str(req['id']) + req['api_key'] + param__string + str(req['nonce'])

            req['sig'] = hmac.new(
                bytes(str(SECRET_KEY), 'utf-8'),
                msg=bytes(sig_pay_load, 'utf-8'),
                digestmod=hashlib.sha256
            ).hexdigest()

        except Exception as e:
            print("Error GetAccountSummary:\n %s" % json_string_utf8)
            print(e)

        return json_string_utf8
