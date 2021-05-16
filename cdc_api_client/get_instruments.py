from api.get_instruments import GetInstruments


def main():
    url = "https://api.crypto.com/v2/public/get-instruments"
    instruments = GetInstruments(url)
    response = instruments.do_get()
    instruments_list = instruments.parse_response(response)

    print(f"API url '{url}'")
    print(f"API Response '{response.status_code}' - '{response.reason}'\n")
    response_json_result = response.json()['result']
    print(response_json_result)

    print("\nAPI Response list:")
    print(instruments_list)
    for instrument in instruments_list:
        print(instrument)

    print("\nAPI Response Instruments:")
    for instrument in instruments_list:
        instrument_name = instrument.get_instrument_name()
        quote_currency = instrument.get_quote_currency()
        base_currency = instrument.get_base_currency()
        price_decimals = instrument.get_price_decimals()
        quantity_decimals = instrument.get_quantity_decimals()
        margin_trading_enabled = instrument.get_margin_trading_enabled()

        print(f"instrument_name:        {instrument_name}")
        print(f"quote_currency:         {quote_currency}")
        print(f"base_currency:          {base_currency}")
        print(f"price_decimals:         {price_decimals}")
        print(f"quantity_decimals:      {quantity_decimals}")
        print(f"margin_trading_enabled: {margin_trading_enabled}")
        print("")


if __name__ == "__main__":
    main()
