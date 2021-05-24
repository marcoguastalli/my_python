import requests
from bnc_api_client.api_request import ApiRequest


# 24hr Ticker Price Change Statistics
# 24 hour rolling window price change statistics. Careful when accessing this with no symbol.
# https://binance-docs.github.io/apidocs/spot/en/#current-average-price
#
# url = https://api.binance.com/api/v3/ticker/24h
#     = https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT
class GetTicker(ApiRequest):
    def __init__(self, url):
        super().__init__(url, None, None)

    def do_get(self):
        response = None
        try:
            headers = {'Content-type': 'application/json'}
            response = requests.get(self.url, headers=headers)

        except Exception as e:
            print("Error get-ticker")
            print(e)

        return response

    @staticmethod
    def parse_response(api_response: requests.models.Response):
        result: dict = {}

        json_response = api_response.json()
        for ticker in json_response:
            pair = ticker['symbol']
            result[pair] = ticker
        return result
