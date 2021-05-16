from api.get_candlestick import GetCandleStick


def main():
    instrument_name = 'BTC_USDT'
    timeframe = '5m'
    url = f'https://api.crypto.com/v2/public/get-candlestick?instrument_name={instrument_name}&timeframe={timeframe}'
    candlestick = GetCandleStick(url)
    response = candlestick.do_get()

    print(f"API url '{url}'")
    print(f"API Response '{response.status_code}' - '{response.reason}'\n")
    response_json_result = response.json()['result']
    print(response_json_result)


if __name__ == "__main__":
    main()
