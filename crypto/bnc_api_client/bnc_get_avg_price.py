from api.get_avg_price import GetAveragePrice

SYMBOL = 'BTCUSDT'


def main():
    url = "https://api.binance.com/api/v3/avgPrice"
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
