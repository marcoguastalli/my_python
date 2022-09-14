import requests
from api.api_request import ApiRequest


# Get Staking Product List
# Get available Staking product list
# https://binance-docs.github.io/apidocs/spot/en/#get-staking-product-list-user_data
#
# url = /sapi/v1/staking/productList
class GetStakingProductList(ApiRequest):
    def __init__(self, url, api_key, secret_key):
        super().__init__(url, api_key, secret_key)

    def do_get(self):
        response = None
        try:
            headers = {'Content-type': 'application/json'}
            response = requests.get(self.url + "?product=STAKING", headers=headers)

        except Exception as e:
            print("Error get-staking-product-data")
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
