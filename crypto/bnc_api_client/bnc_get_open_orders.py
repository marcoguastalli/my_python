from dotenv import dotenv_values

from api.get_open_orders import GetOpenOrders

REST_API_ENDPOINT_SANDBOX = "https://testnet.binance.vision"
REST_API_ENDPOINT_PRODUCTION = "https://api.binance.com"
REST_API_ENDPOINT = REST_API_ENDPOINT_PRODUCTION
SYMBOL = 'BTCUSDT'


def main():
    url = REST_API_ENDPOINT + "/api/v3/openOrders"
    config = dotenv_values(".env")
    open_orders = GetOpenOrders(url, config['API_KEY'], config['API_SECRET'])
    response = open_orders.do_get(SYMBOL)
    response_list = open_orders.parse_response(response)

    print(f"API url '{url}'")
    print(f"API Response '{response.status_code}' - '{response.reason}'\n")
    print("API Response json:")
    print(response.json())

    if response_list.__len__() > 0:
        print(f"\nOpen Orders for symbol {SYMBOL}:")
        for order in response_list:
            print(f"Symbol   : '{order['symbol']}'")
            print(f" orderId : '{order['orderId']}'")
            print(f" type    : '{order['type']}'")
            print(f" side    : '{order['side']}'")
            print(f" price   : '{order['price']}'")
            print(f" quantity: '{order['origQty']}'")


if __name__ == "__main__":
    main()
