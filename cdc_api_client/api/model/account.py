class Account:

    def __init__(self, currency, balance, available, order, stake):
        self.currency = currency
        self.balance = balance
        self.available = available
        self.order = order
        self.stake = stake

    def get_currency(self):
        return self.currency

    def get_balance(self):
        return self.balance

    def get_available(self):
        return self.available

    def get_order(self):
        return self.order

    def get_stake(self):
        return self.stake

    def __str__(self):
        result = '{' \
                 + '"currency":"' + self.currency + '",' \
                 + '"balance" :' + str(self.balance) + ',' \
                 + '"available": ' + str(self.available) + ',' \
                 + '"order": ' + str(self.order) + ',' \
                 + '"stake": ' + str(self.stake) \
                 + "}"
        return result
