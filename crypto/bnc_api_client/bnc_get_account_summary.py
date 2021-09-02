from datetime import datetime

from dotenv import dotenv_values

from api.get_account_summary import GetAccountSummary
from api.get_ticker import GetTicker

REST_API_ENDPOINT_SANDBOX = "https://testnet.binance.vision"
REST_API_ENDPOINT_PRODUCTION = "https://api.binance.com"
REST_API_ENDPOINT = REST_API_ENDPOINT_PRODUCTION


def main():
    ticker = GetTicker(REST_API_ENDPOINT + '/api/v3/ticker/24hr')
    response = ticker.do_get()
    tickers_dictionary = ticker.parse_response(response)

    config = dotenv_values(".env")
    url = REST_API_ENDPOINT + "/api/v3/account"
    print("Reading account from API url '%s' at '%s'" % (url, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")))

    account_summary = GetAccountSummary(url, config['API_KEY'], config['API_SECRET'])
    response = account_summary.do_get()
    if type(response) is str:
        print("API Error: %s" % response)
    else:
        # response should be type 'requests.models.Response'
        print(f"API Response '{response.status_code}' - '{response.reason}'\n")
        # parse response
        accounts = account_summary.parse_response(response)

        pair_account_balance_dictionary = {}
        for account in accounts:
            currency = account.get_currency()
            balance = account.get_balance()
            locked = account.get_locked()
            total_balance = balance + locked
            if total_balance > 0:
                if currency == 'USDT':
                    pair_account_balance_dictionary[currency] = account, total_balance
                    pass
                elif currency[0:2] == "LD":
                    pair = currency[2:] + 'USDT'
                    add_pair_to_account_balance_dictionary(tickers_dictionary, account, pair, total_balance, pair_account_balance_dictionary)
                    pass
                elif currency == "BETH":
                    pair = "ETHUSDC"
                    add_pair_to_account_balance_dictionary(tickers_dictionary, account, pair, total_balance, pair_account_balance_dictionary)
                    pass
                else:
                    # the account currency + "USDT" gives a pair
                    pair = currency + "USDT"
                    add_pair_to_account_balance_dictionary(tickers_dictionary, account, pair, total_balance, pair_account_balance_dictionary)
                    pass
        # calculate total_balance
        total_balance = 0
        for key, value in pair_account_balance_dictionary.items():
            if key != value:
                pair = key
                account = value[0]
                pair_balance = value[1]
                # print(key, ': ', value)
                balance_to_print = "{:f}".format(account.get_balance() + account.get_locked())
                print(f"The balance for currency '{account.get_currency()}' is {balance_to_print}, the balance for pair '{pair}' in USDT is: {pair_balance}")
                # add to total
                total_balance += pair_balance
        # print total
        print("The total balance for the account is %s USDT" % total_balance)


def add_pair_to_account_balance_dictionary(tickers_dictionary, account, pair, total_balance, pair_account_balance_dictionary):
    try:
        # from the tickers_dictionary get the corresponding pair
        ticker = tickers_dictionary[pair]
        # a is the price of the latest trade, null if there weren't any trades
        latest_trade_price = float(ticker['lastPrice'])
        if latest_trade_price is not None:
            # multiply the price from the ticker with balance from the account
            pair_balance = latest_trade_price * total_balance
            # add to pair_balance_dictionary
            pair_account_balance_dictionary[pair] = account, pair_balance
    except KeyError:
        print("No ticker found for pair: '%s'" % pair)
        pass


if __name__ == "__main__":
    main()
