from dotenv import dotenv_values

from api.post_new_order import PostNewOrder

SYMBOL = 'BTCUSDT'


def main():
    url = "https://api.binance.com/api/v3/order/test"
    config = dotenv_values(".env")
    post_new_order = PostNewOrder(url, config['API_KEY'], config['API_SECRET'])
    response = post_new_order.do_post(SYMBOL)
    response_json = post_new_order.parse_response(response)

    print(f"API url '{url}'")
    print(f"API Response '{response.status_code}' - '{response.reason}'\n")
    print("API Response json:")
    print(response.json())

    print(f"\nSymbol {SYMBOL}: {response_json['symbol']}")


if __name__ == "__main__":
    main()
