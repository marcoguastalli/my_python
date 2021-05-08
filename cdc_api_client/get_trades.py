from api.get_trades import GetTrades

instrument_name = 'BTC_USDT'


def main():
    url = f'https://api.crypto.com/v2/public/get-trades?instrument_name={instrument_name}'
    trades = GetTrades(url)
    response = trades.do_get()
    # response should be type 'requests.models.Response'
    print(f"API Response '{response.status_code}' - '{response.reason}'\n")
    response_json_result = response.json()['result']
    print(response_json_result)


if __name__ == "__main__":
    main()
