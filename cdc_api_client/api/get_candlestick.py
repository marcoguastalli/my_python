import requests
from api.api_request import ApiRequest


# Retrieves candlesticks (k-line data history) over a given period for an instrument (e.g. BTC_USDT)
# https://exchange-docs.crypto.com/spot/index.html#public-get-candlestick
#
# url = https://api.crypto.com/v2/public/get-candlestick?instrument_name=BTC_USDT&timeframe=5m
class GetCandleStick(ApiRequest):
    def __init__(self, url):
        super().__init__(url, None, None)

    def do_get(self):
        response = None
        try:
            headers = {'Content-type': 'application/json'}
            response = requests.get(self.url, headers=headers)

        except Exception as e:
            print("Error GetCandleStick:\n %s" % req)
            print(e)

        return response
