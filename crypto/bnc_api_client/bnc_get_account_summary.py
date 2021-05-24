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


if __name__ == "__main__":
    main()
