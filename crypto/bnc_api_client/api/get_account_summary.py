import json
import time

import requests
from api.api_request import ApiRequest
from api.model.account import Account

from .utils.sign_request import sign_request


# Get current account information.
# https://binance-docs.github.io/apidocs/spot/en/#query-open-oco-user_data
#
# url = https://api.binance.com/api/v3/account
# adding the http-headers
#
# The response is a list of accounts
class GetAccountSummary(ApiRequest):
    def __init__(self, url, api_key, secret_key):
        super().__init__(url, api_key, secret_key)

    def do_get(self):
        response = None
        try:
            params_dict = {
                "recvWindow": 5000,
                "timestamp": int(time.time() * 1000)
            }
            query_string = sign_request(params_dict, self.api_key, self.secret_key)
            if query_string is not None:
                url = self.url + "?" + query_string
                print(f"Reading account from API url '{url}'")
                headers = {'Content-Type': 'application/json;charset=utf-8', 'X-MBX-APIKEY': self.api_key}
                response = requests.get(url, headers=headers)
            else:
                return "Invalid Request"

        except Exception as e:
            print("Error get-account-summary")
            print(e)

        return response

    # Returns the account balance of a user for a particular token
    # https://exchange-docs.crypto.com/spot/index.html#private-get-account-summary
    #
    # The response is a list of accounts
    # For each account in the list the object Account is created and added to the returned account_list
    @staticmethod
    def parse_response(api_response: requests.models.Response):
        json_response = api_response.json()
        json_response_result = json_response['result']
        accounts = json_response_result['accounts']
        result: list = []
        for account in accounts:
            result.append(Account(account['currency'], account['balance'], account['available'], account['order'], account['stake']))
        return result
