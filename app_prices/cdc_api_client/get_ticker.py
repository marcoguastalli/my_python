import requests
from cdc_api_client.api_request import ApiRequest


# Fetches the public tickers for an instrument (e.g. BTC_USDT).
# instrument_name can be omitted to show tickers for all instruments
# https://exchange-docs.crypto.com/spot/index.html#public-get-ticker
#
# url = https://api.crypto.com/v2/public/get-ticker
#     = https://api.crypto.com/v2/public/get-ticker?instrument_name=BTC_USDT
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
