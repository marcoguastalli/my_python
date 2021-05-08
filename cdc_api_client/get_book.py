from api.get_book import GetBook

instrument_name = 'BTC_USDT'
depth = 1


def main():
    url = f"https://api.crypto.com/v2/public/get-book?instrument_name={instrument_name}&depth={depth}"
    book = GetBook(url)
    response = book.do_get()
    # response should be type 'requests.models.Response'
    print("API Response '%s' - '%s'" % (response.status_code, response.reason))
    response_json_result = response.json()['result']
    print(response_json_result)


if __name__ == "__main__":
    main()
