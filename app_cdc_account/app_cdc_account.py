from api.get_account_summary import GetAccountSummary
from utils.py_utils_date import get_current_datetime_as_int

REST_API_ENDPOINT_SANDBOX = "https://uat-api.3ona.co/v2/"
REST_API_ENDPOINT_PRODUCTION = "https://api.crypto.com/v2/"
REST_API_ENDPOINT = REST_API_ENDPOINT_SANDBOX
REST_API_KEY = ""
REST_API_SECRET = ""


def main():
    print("Reading account from API url '%s'" % REST_API_ENDPOINT)
    current_timestamp = get_current_datetime_as_int()

    account_summary = GetAccountSummary(REST_API_ENDPOINT, REST_API_KEY, REST_API_SECRET)
    response = account_summary.do_post("27", "CRO")
    print(response)


if __name__ == "__main__":
    main()
