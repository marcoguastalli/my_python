from datetime import datetime

from api.get_exchangeInfo import GetExchangeInformation

REST_API_ENDPOINT_SANDBOX = "https://testnet.binance.vision"
REST_API_ENDPOINT_PRODUCTION = "https://api.binance.com"
REST_API_ENDPOINT = REST_API_ENDPOINT_PRODUCTION


def main():
    url = REST_API_ENDPOINT + '/api/v3/exchangeInfo'
    print("Reading exchange information from API url '%s' at '%s'" % (url, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")))
    exchange_info = GetExchangeInformation(url)
    response = exchange_info.do_get()
    symbols_dictionary = exchange_info.parse_response(response)
    for symbol in symbols_dictionary:
        symbol_item = symbols_dictionary.get(symbol)
        print(f"{symbol} --> {symbol_item['baseAsset']}_{symbol_item['quoteAsset']}")


if __name__ == "__main__":
    main()
