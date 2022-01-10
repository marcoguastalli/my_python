import time

import requests
from api.api_request import ApiRequest

from .utils.sign_request import sign_request


# Send in a new order.
# https://binance-docs.github.io/apidocs/spot/en/#new-order-trade
#
# url = /api/v3/order
class PostNewOrder(ApiRequest):
    def __init__(self, url, api_key, secret_key):
        super().__init__(url, api_key, secret_key)

    def do_post(self, symbol, side, type, quantity, quoteOrderQty):
        response = None
        try:
            params_dict = {
                "recvWindow": 60000,
                "timestamp": int(time.time() * 1000),
                "symbol": symbol,
                "side": side,
                "type": type,
                "quantity": quantity
            }
            query_string = sign_request(params_dict, self.api_key, self.secret_key)
            if query_string is not None:
                url = self.url + "?" + query_string
                print(f"Posting new order to API url '{url}'")
                headers = {'Content-Type': 'application/json;charset=utf-8', 'X-MBX-APIKEY': self.api_key}
                response = requests.post(url, headers=headers)
            else:
                return "Invalid Request"

        except Exception as e:
            print("Error post new order")
            print(e)

        return response

    @staticmethod
    def parse_response(api_response: requests.models.Response):
        result: dict = {}

        json_response = api_response.json()
        if json_response is not None:
            result = json_response
        return result
