from api.get_book import GetBook


def main():
    instrument_name = 'BTC_USDT'
    depth = 2
    url = f'https://api.crypto.com/v2/public/get-book?instrument_name={instrument_name}&depth={depth}'
    book = GetBook(url)
    response = book.do_get()
    book_dictionary = book.parse_response(response)

    print(f"API url '{url}'")
    print(f"API Response '{response.status_code}' - '{response.reason}'\n")
    print("API Response json:")
    print(response.json())
    print("\nAPI Response result:")
    response_json_result = response.json()['result']
    print(response_json_result)

    print("\nAPI Response dictionary:")
    print(book_dictionary)

    instrument_name_resp = book_dictionary['instrument_name']
    depth_resp = book_dictionary['depth']
    bids_list = book_dictionary['bids']
    asks_list = book_dictionary['asks']
    book_timestamp = book_dictionary['book_timestamp']

    print(f"instrument_name: {instrument_name_resp}")
    print(f"depth:           {depth_resp}")
    print(f"book_timestamp:  {book_timestamp}")
    for bid in bids_list:
        print("Bids:")
        print(f"    Price:            {bid[0]}")
        print(f"    Quantity:         {bid[1]}")
        print(f"    Number of Orders: {bid[2]}")
    for ask in asks_list:
        print("Asks:")
        print(f"    Price:            {ask[0]}")
        print(f"    Quantity:         {ask[1]}")
        print(f"    Number of Orders: {ask[2]}")


if __name__ == "__main__":
    main()
