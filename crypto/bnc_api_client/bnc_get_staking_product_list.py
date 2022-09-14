from datetime import datetime

from dotenv import dotenv_values
from api.get_staking_product_list import GetStakingProductList

REST_API_ENDPOINT_SANDBOX = "https://testnet.binance.vision"
REST_API_ENDPOINT_PRODUCTION = "https://api.binance.com"
REST_API_ENDPOINT = REST_API_ENDPOINT_PRODUCTION


def main():
    url = REST_API_ENDPOINT + "/sapi/v1/staking/productList"
    config = dotenv_values(".env")
    print("Reading Staking Product List from API url '%s' at '%s'" % (url, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")))

    staking_product_list = GetStakingProductList(url, config['API_KEY'], config['API_SECRET'])
    response = staking_product_list.do_get()
    if response.status_code != 200:
        print(f"API url '{url}'")
        print(f"API Response '{response.status_code}' - '{response.json()}'\n")
    else:
        todo = staking_product_list.parse_response(response)
        print(f"API url '{url}'")
        print(f"API Response '{response.status_code}' - '{response.reason}'\n")
        print("API Response json:")
        print(response.json())


if __name__ == "__main__":
    main()
