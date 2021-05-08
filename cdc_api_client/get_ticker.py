from api.get_ticker import GetTicker


def main():
    url = "https://api.crypto.com/v2/public/get-ticker"
    ticker = GetTicker(url)
    response = ticker.do_get()
    tickers_dictionary = ticker.parse_response(response)

    print(f"API url '{url}'")
    print(f"API Response '{response.status_code}' - '{response.reason}'\n")
    print("API Response json:")
    print(response.json())
    print("\nAPI Response result:")
    response_json_result = response.json()['result']
    print(response_json_result)

    print("\nAPI Response dictionary:")
    print(tickers_dictionary)

    print("\nAPI Response dictionary Ticker:")
    ticker = tickers_dictionary['BTC_USDT']
    print(ticker)
    print("")
    pair = ticker['i']
    current_best_bid_price = ticker['b']
    current_best_ask_price = ticker['k']
    latest_trade_price = ticker['a']
    ticker_timestamp = ticker['t']
    total_24h_traded_volume = ticker['v']
    price_of_the_24h_highest_trade = ticker['h']
    price_of_the_24h_lowest_trade = ticker['l']
    price_change_24h = ticker['c']

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
