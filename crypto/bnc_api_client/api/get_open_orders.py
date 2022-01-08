import time

import requests
from api.api_request import ApiRequest

from .utils.sign_request import sign_request


# Get current account information.
# https://binance-docs.github.io/apidocs/spot/en/#current-open-orders-user_data
#
# url = https://api.binance.com/api/v3/openOrders
# adding the http-headers
#
# The response is a list of orders
class GetOpenOrders(ApiRequest):
    def __init__(self, url, api_key, secret_key):
        super().__init__(url, api_key, secret_key)

    def do_get(self, symbol):
        response = None
        try:
            params_dict = {
                "recvWindow": 60000,
                "timestamp": int(time.time() * 1000),
                "symbol": symbol
            }
            query_string = sign_request(params_dict, self.api_key, self.secret_key)
            if query_string is not None:
                url = self.url + "?" + query_string
                print(f"Reading open orders from API url '{url}'")
                headers = {'Content-Type': 'application/json;charset=utf-8', 'X-MBX-APIKEY': self.api_key}
                response = requests.get(url, headers=headers)
            else:
                return "Invalid Request"

        except Exception as e:
            print("Error Get Open Orders")
            print(e)

        return response

    @staticmethod
    def parse_response(api_response: requests.models.Response):
        result: list = []

        json_response = api_response.json()
        for order in json_response:
            result.append(order)
        return result
