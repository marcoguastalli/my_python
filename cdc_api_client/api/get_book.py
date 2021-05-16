import requests
from api.api_request import ApiRequest


# Fetches the public order book for a particular instrument and depth
# https://exchange-docs.crypto.com/spot/index.html#public-get-book
#
# url = https://api.crypto.com/v2/public/get-book?instrument_name=BTC_USDT&depth=1
class GetBook(ApiRequest):
    def __init__(self, url):
        super().__init__(url, None, None)

    def do_get(self):
        response = None
        try:
            headers = {'Content-type': 'application/json'}
            response = requests.get(self.url, headers=headers)

        except Exception as e:
            print("Error get-book")
            print(e)

        return response

    @staticmethod
    def parse_response(api_response: requests.models.Response):
        result: dict = {}

        json_response = api_response.json()
        json_response_result = json_response['result']
        instrument_name = json_response_result['instrument_name']
        depth = json_response_result['depth']

        result['instrument_name'] = instrument_name
        result['depth'] = depth

        data = json_response_result['data']
        for book in data:
            bids = book['bids']
            asks = book['asks']
            book_timestamp = book['t']

            result['bids'] = bids
            result['asks'] = asks
            result['book_timestamp'] = book_timestamp
        return result
