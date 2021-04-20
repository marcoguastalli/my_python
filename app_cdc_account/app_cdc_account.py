from datetime import datetime

from dotenv import dotenv_values

from api.get_account_summary import GetAccountSummary

REST_API_ENDPOINT_SANDBOX = "https://uat-api.3ona.co/v2/"
REST_API_ENDPOINT_PRODUCTION = "https://api.crypto.com/v2/"
REST_API_ENDPOINT = REST_API_ENDPOINT_PRODUCTION


def main():
    config = dotenv_values(".env")
    print(type(config))
    url = REST_API_ENDPOINT + "private/get-account-summary"
    print("Reading account from API url '%s' at '%s'" % (url, datetime.utcnow()))

    account_summary = GetAccountSummary(url, config['API_KEY'], config['API_SECRET'])
    response = account_summary.do_post()
    if type(response) is not str:
        print(response.status_code, response.reason)
        print(response.content)
    else:
        print(response)


if __name__ == "__main__":
    main()
