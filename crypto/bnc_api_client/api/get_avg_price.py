import requests
from api.api_request import ApiRequest


# Current average price for a symbol.
# https://binance-docs.github.io/apidocs/spot/en/#24hr-ticker-price-change-statistics
#
# url = https://api.binance.com/api/v3/avgPrice?symbol=BTCUSDT
class GetAveragePrice(ApiRequest):
    def __init__(self, url):
        super().__init__(url, None, None)

    def do_get(self, symbol):
        response = None
        try:
            headers = {'Content-type': 'application/json'}
            response = requests.get(self.url + "?symbol=" + symbol, headers=headers)

        except Exception as e:
            print("Error API")
            print(e)

        return response

    @staticmethod
    def parse_response(api_response: requests.models.Response):
        result: dict = {}

        json_response = api_response.json()
        if json_response is not None:
            result['price'] = json_response['price']
        return result
