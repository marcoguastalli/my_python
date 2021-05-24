from api.get_ticker import GetTicker


def main():
    url = "https://api.binance.com/api/v3/ticker/24hr"
    ticker = GetTicker(url)
    response = ticker.do_get()
    tickers_dictionary = ticker.parse_response(response)

    print(f"API url '{url}'")
    print(f"API Response '{response.status_code}' - '{response.reason}'\n")
    print("API Response json:")
    print(response.json())

    print("\nAPI Response dictionary:")
    for key, value in tickers_dictionary.items():
        print(f"\nPair '{key}': {value}")

    print("\nAPI Response dictionary Ticker:")
    ticker = tickers_dictionary['BTCUSDT']
    print(ticker)
    print("")
    pair = ticker['symbol']
    current_best_bid_price = ticker['bidPrice']
    current_best_ask_price = ticker['askPrice']
    latest_trade_price = ticker['lastPrice']
    ticker_timestamp = ticker['openTime']
    total_24h_traded_volume = ticker['volume']
    price_of_the_24h_highest_trade = ticker['highPrice']
    price_of_the_24h_lowest_trade = ticker['lowPrice']
    price_change_24h = ticker['priceChange']

    print(f"pair:                           {pair}")
    print(f"current_best_bid_price:         {current_best_bid_price}")
    print(f"current_best_ask_price:         {current_best_ask_price}")
    print(f"latest_trade_price:             {latest_trade_price}")
    print(f"ticker_timestamp:               {ticker_timestamp}")
    print(f"total_24h_traded_volume:        {total_24h_traded_volume}")
    print(f"price_of_the_24h_highest_trade: {price_of_the_24h_highest_trade}")
    print(f"price_of_the_24h_lowest_trade:  {price_of_the_24h_lowest_trade}")
    print(f"price_change_24h:               {price_change_24h}")


if __name__ == "__main__":
    main()
