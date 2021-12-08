import requests


# Get Current exchange trading rules and symbol information.
# https://binance-docs.github.io/apidocs/spot/en/#exchange-information
#
# url = https://api.binance.com/api/v3/exchangeInfo
# adding the http-headers
#
# The response is a list of symbols
class GetExchangeInformation:
    def __init__(self, url):
        self.url = url

    def do_get(self):
        response = None
        try:
            headers = {'Content-type': 'application/json'}
            response = requests.get(self.url, headers=headers)

        except Exception as e:
            print("Error get-exchangeInfo")
            print(e)

        return response

    @staticmethod
    def parse_response(api_response: requests.models.Response):
        result: dict = {}

        json_response = api_response.json()
        symbols = json_response['symbols']
        print(f"Found {len(symbols)} symbols in the Exchange")
        for symbol_item in symbols:
            result[symbol_item['symbol']] = symbol_item
        print(f"Return {len(symbols)} symbols from the API")
        return result
