from datetime import datetime

from dotenv import dotenv_values

from api.get_account_summary import GetAccountSummary
from api.get_ticker import GetTicker

REST_API_ENDPOINT_SANDBOX = "https://uat-api.3ona.co/v2/"
REST_API_ENDPOINT_PRODUCTION = "https://api.crypto.com/v2/"
REST_API_ENDPOINT = REST_API_ENDPOINT_PRODUCTION
# https://es.investing.com/currencies/usd-eur
USD_EUR = 0.8419


def main():
    ticker = GetTicker(REST_API_ENDPOINT + 'public/get-ticker')
    response = ticker.do_get()
    tickers_dictionary = ticker.parse_response(response)

    config = dotenv_values(".env")
    url = REST_API_ENDPOINT + "private/get-account-summary"
    print("Reading account from API url '%s' at '%s'" % (url, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")))

    account_summary = GetAccountSummary(url, config['API_KEY'], config['API_SECRET'])
    response = account_summary.do_post()
    if type(response) is str:
        print("API Error: %s" % response)
    else:
        # response should be type 'requests.models.Response'
        print(f"API Response '{response.status_code}' - '{response.reason}'\n")
        # parse response
        accounts = account_summary.parse_response(response)

        pair_account_balance_dictionary = {}
        for account in accounts:
            balance = account.get_balance()
            currency = account.get_currency()
            if balance > 0 and currency != 'USDT':
                # the account currency + "_USDT" gives a pair
                pair = currency + "_USDT"
                try:
                    # from the tickers_dictionary get the corresponding pair
                    ticker = tickers_dictionary[pair]
                    # a is the price of the latest trade, null if there weren't any trades
                    latest_trade_price = ticker['a']
                    if latest_trade_price is not None:
                        # multiply the price from the ticker with balance from the account
                        pair_balance = latest_trade_price * balance
                        # add to pair_balance_dictionary
                        pair_account_balance_dictionary[pair] = account, pair_balance
                except KeyError:
                    print("No ticker found for pair: '%s'" % pair)
                    pass
            elif currency == 'USDT':
                pair_account_balance_dictionary[currency] = account, balance
                pass
        # calculate total_balance
        total_balance_usdt = 0
        total_balance_euro = 0
        for key, value in pair_account_balance_dictionary.items():
            if key != value:
                pair = key
                account = value[0]
                pair_balance = value[1]
                # print(key, ': ', value)
                balance_to_print = "{:f}".format(account.get_balance())
                print(f"The balance for currency '{account.get_currency()}' is {balance_to_print}, the balance for pair '{pair}' in USDT is: {pair_balance}, in EUR is {USD_EUR * pair_balance}")
                # add to total
                total_balance_usdt += pair_balance
                total_balance_euro += (USD_EUR * pair_balance)
        # print total
        print("The total balance for the account is %s USDT" % total_balance_usdt)
        print("The total balance for the account is %s EURO" % total_balance_euro)


if __name__ == "__main__":
    main()
