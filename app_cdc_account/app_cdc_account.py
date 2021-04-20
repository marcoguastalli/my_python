from datetime import datetime

from dotenv import dotenv_values

from api.get_account_summary import GetAccountSummary
from api.parse_account_summary import ParseAccountSummary

REST_API_ENDPOINT_SANDBOX = "https://uat-api.3ona.co/v2/"
REST_API_ENDPOINT_PRODUCTION = "https://api.crypto.com/v2/"
REST_API_ENDPOINT = REST_API_ENDPOINT_PRODUCTION


def main():
    config = dotenv_values(".env")
    url = REST_API_ENDPOINT + "private/get-account-summary"
    print("Reading account from API url '%s' at '%s'" % (url, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")))

    account_summary = GetAccountSummary(url, config['API_KEY'], config['API_SECRET'])
    response = account_summary.do_post()
    if type(response) is str:
        print("API Error: %s" % response)
    else:
        # response should be type 'requests.models.Response'
        print("API Response '%s' - '%s'" % (response.status_code, response.reason))

        parser = ParseAccountSummary(response)
        accounts = parser.get_account_list()
        for account in accounts:
            print(account)


if __name__ == "__main__":
    main()
