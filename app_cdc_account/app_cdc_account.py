from api.get_account_summary import GetAccountSummary
from utils.py_utils_date import get_current_datetime_as_int

REST_API_ENDPOINT_SANDBOX = "https://uat-api.3ona.co/v2/"
REST_API_ENDPOINT_PRODUCTION = "https://api.crypto.com/v2/"
REST_API_ENDPOINT = REST_API_ENDPOINT_PRODUCTION
REST_API_KEY = ""
REST_API_SECRET = ""


def main():
    url = REST_API_ENDPOINT + "private/get-account-summary"
    current_timestamp = get_current_datetime_as_int()
    print("Reading account from API url '%s' at '%s'" % (REST_API_ENDPOINT, current_timestamp))

    account_summary = GetAccountSummary(url, REST_API_KEY, REST_API_SECRET)
    response = account_summary.do_post("1", "CRO")
    print(response)


if __name__ == "__main__":
    main()
