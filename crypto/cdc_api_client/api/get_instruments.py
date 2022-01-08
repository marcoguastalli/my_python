import json

import requests
from api.api_request import ApiRequest
from api.model.instrument import Instrument


# Provides information on all supported instruments (e.g. BTC_USDT)
# https://exchange-docs.crypto.com/spot/index.html#public-get-instruments
#
# url = https://api.crypto.com/v2/public/get-instruments
class GetInstruments(ApiRequest):
    def __init__(self, url):
        super().__init__(url, None, None)

    def do_get(self):
        response = None
        try:
            req = {"id": 1, "method": "public/get-instruments", "nonce": super().get_nonce()}
            headers = {'Content-type': 'application/json'}
            response = requests.get(self.url, headers=headers, data=json.dumps(req))

        except Exception as e:
            print("Error get-instruments")
            print(e)

        return response

    @staticmethod
    def parse_response(api_response: requests.models.Response):
        result: list = []

        json_response = api_response.json()
        json_response_result = json_response['result']
        instruments = json_response_result['instruments']
        for instrument in instruments:
            instrument_name = instrument['instrument_name']
            quote_currency = instrument['quote_currency']
            base_currency = instrument['base_currency']
            price_decimals = instrument['price_decimals']
            quantity_decimals = instrument['quantity_decimals']
            margin_trading_enabled = instrument['margin_trading_enabled']

            result.append(Instrument(instrument_name, quote_currency, base_currency, price_decimals, quantity_decimals, margin_trading_enabled))
        return result
