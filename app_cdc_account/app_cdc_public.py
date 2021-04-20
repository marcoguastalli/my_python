from api.get_instruments import GetInstruments
from api.get_ticker import GetTicker


def main():
    instruments = GetInstruments('https://api.crypto.com/v2/public/get-instruments')
    response = instruments.do_get()
    # response should be type 'requests.models.Response'
    print("API Response '%s' - '%s'" % (response.status_code, response.reason))

    ticker = GetTicker('https://api.crypto.com/v2/public/get-ticker')
    response = ticker.do_get()
    # response should be type 'requests.models.Response'
    print("API Response '%s' - '%s'" % (response.status_code, response.reason))


if __name__ == "__main__":
    main()
