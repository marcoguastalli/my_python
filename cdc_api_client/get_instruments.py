from api.get_instruments import GetInstruments


def main():
    instruments = GetInstruments('https://api.crypto.com/v2/public/get-instruments')
    response = instruments.do_get()
    # response should be type 'requests.models.Response'
    print("API Response '%s' - '%s'" % (response.status_code, response.reason))
    response_json_result = response.json()['result']
    print(response_json_result)


if __name__ == "__main__":
    main()