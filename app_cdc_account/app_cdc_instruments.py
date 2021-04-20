from api.get_instruments import GetInstruments

URL = "https://api.crypto.com/v2/public/get-instruments"


def main():
    instruments = GetInstruments(URL)
    response = instruments.do_get()
    # response should be type 'requests.models.Response'
    print("API Response '%s' - '%s'" % (response.status_code, response.reason))


if __name__ == "__main__":
    main()
