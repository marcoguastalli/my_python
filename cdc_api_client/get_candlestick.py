from api.get_candlestick import GetCandleStick

instrument_name = 'BTC_USDT'
timeframe = '5m'


def main():
    url = f'https://api.crypto.com/v2/public/get-candlestick?instrument_name={instrument_name}&timeframe={timeframe}'
    candlestick = GetCandleStick(url)
    response = candlestick.do_get()
    # response should be type 'requests.models.Response'
    print("API Response '%s' - '%s'" % (response.status_code, response.reason))
    response_json_result = response.json()['result']
    print(response_json_result)


if __name__ == "__main__":
    main()
