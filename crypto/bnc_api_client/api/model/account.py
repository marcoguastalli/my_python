class Account:

    def __init__(self, currency, balance, locked):
        self.currency = currency
        self.balance = balance
        self.locked = locked

    def get_currency(self):
        return self.currency

    def get_balance(self):
        return self.balance

    def get_locked(self):
        return self.locked

    def __str__(self):
        result = '{' \
                 + '"currency":"' + self.currency + '",' \
                 + '"balance" :' + str(self.balance) + ',' \
                 + '"locked": ' + str(self.locked) \
                 + "}"
        return result
