import json
import time

import requests
from api.api_request import ApiRequest
from api.model.account import Account

from .utils.sign_request import sign_request


# Returns the account balance of a user for a particular token
# https://exchange-docs.crypto.com/spot/index.html#private-get-account-summary
#
# POST to url = https://api.crypto.com/v2/private/get-account-summary
# adding the request-headers
#
# The response is a list of accounts
class GetAccountSummary(ApiRequest):
    def __init__(self, url, api_key, secret_key):
        super().__init__(url, api_key, secret_key)

    def do_post(self):
        response = None
        try:
            params_dict = {
                "id": 1,
                "method": "private/get-account-summary",
                "api_key": self.api_key,
                "params": {},
                "nonce": int(time.time() * 1000)
            }
            params_dict = sign_request(params_dict, self.api_key, self.secret_key)
            if params_dict is not None:
                headers = {'Content-type': 'application/json'}
                response = requests.post(self.url, headers=headers, data=json.dumps(params_dict))
            else:
                return "Invalid Request"

        except Exception as e:
            print("Error get-account-summary")
            print(e)

        return response

    # The response is a list of accounts
    # For each element in the list the object Account is created and added to the returned list
    @staticmethod
    def parse_response(api_response: requests.models.Response):
        json_response = api_response.json()
        json_response_result = json_response['result']
        accounts = json_response_result['accounts']
        result: list = []
        for account in accounts:
            result.append(Account(account['currency'], account['balance'], account['available'], account['order'], account['stake']))
        return result
