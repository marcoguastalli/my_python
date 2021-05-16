import json

import requests
from api.api_request import ApiRequest


# Fetches the public trades for a particular instrument
# instrument_name can be omitted to show tickers for all instruments
# https://exchange-docs.crypto.com/spot/index.html#public-get-trades
#
# url = https://api.crypto.com/v2/public/get-trades
#       https://api.crypto.com/v2/public/get-trades?instrument_name=BTC_USDT
class GetTrades(ApiRequest):
    def __init__(self, url):
        super().__init__(url, None, None)

    def do_get(self):
        response = None
        try:
            headers = {'Content-type': 'application/json'}
            response = requests.get(self.url, headers=headers)

        except Exception as e:
            print("Error get-trades")
            print(e)

        return response
