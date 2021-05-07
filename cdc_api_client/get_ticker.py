from api.get_ticker import GetTicker


def main():
    ticker = GetTicker('https://api.crypto.com/v2/public/get-ticker')
    response = ticker.do_get()
    # response should be type 'requests.models.Response'
    print("API Response '%s' - '%s'" % (response.status_code, response.reason))
    response_json_result = response.json()['result']
    print(response_json_result)


if __name__ == "__main__":
    main()
