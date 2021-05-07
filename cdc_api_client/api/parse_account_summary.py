import requests

from api.model.account import Account


# Returns the account balance of a user for a particular token
# https://exchange-docs.crypto.com/spot/index.html#private-get-account-summary
#
# The response is a list of accounts
# For each account in the list the object Account is created and added to the returned account_list
class ParseAccountSummary:
    def __init__(self, api_response: requests.models.Response):
        self.api_response = api_response

    def get_account_list(self):
        json_response = self.api_response.json()
        json_response_result = json_response['result']
        accounts = json_response_result['accounts']
        result: list = []
        for account in accounts:
            result.append(Account(account['currency'], account['balance'], account['available'], account['order'], account['stake']))
        return result
