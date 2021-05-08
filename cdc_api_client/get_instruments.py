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
    for instruments in instruments_list:
        print(instruments)


if __name__ == "__main__":
    main()
