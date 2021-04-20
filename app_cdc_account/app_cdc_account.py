from datetime import datetime

from api.get_account_summary import GetAccountSummary

REST_API_ENDPOINT_SANDBOX = "https://uat-api.3ona.co/v2/"
REST_API_ENDPOINT_PRODUCTION = "https://api.crypto.com/v2/"
REST_API_ENDPOINT = REST_API_ENDPOINT_PRODUCTION
REST_API_KEY = ""
REST_API_SECRET = ""


def main():
    url = REST_API_ENDPOINT + "private/get-account-summary"
    print("Reading account from API url '%s' at '%s'" % (url, datetime.utcnow()))

    account_summary = GetAccountSummary(url, REST_API_KEY, REST_API_SECRET)
    response = account_summary.do_post()
    print(response.status_code, response.reason)
    print(response.content)


if __name__ == "__main__":
    main()
