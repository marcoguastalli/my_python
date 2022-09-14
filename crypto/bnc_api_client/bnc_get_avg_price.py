from api.get_avg_price import GetAveragePrice

SYMBOL = 'BTCUSDT'

REST_API_ENDPOINT_SANDBOX = "https://testnet.binance.vision"
REST_API_ENDPOINT_PRODUCTION = "https://api.binance.com"
REST_API_ENDPOINT = REST_API_ENDPOINT_PRODUCTION


def main():
    url = REST_API_ENDPOINT + "/api/v3/avgPrice"
    average_price = GetAveragePrice(url)
    response = average_price.do_get(SYMBOL)
    response_dictionary = average_price.parse_response(response)

    print(f"API url '{url}'")
    print(f"API Response '{response.status_code}' - '{response.reason}'\n")
    print("API Response json:")
    print(response.json())

    print(f"\nPrice for symbol {SYMBOL}: {response_dictionary['price']}")


if __name__ == "__main__":
    main()
