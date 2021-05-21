class Instrument:

    def __init__(self, instrument_name, quote_currency, base_currency, price_decimals, quantity_decimals, margin_trading_enabled):
        self.instrument_name = instrument_name
        self.quote_currency = quote_currency
        self.base_currency = base_currency
        self.price_decimals = price_decimals
        self.quantity_decimals = quantity_decimals
        self.margin_trading_enabled = margin_trading_enabled

    def get_instrument_name(self):
        return self.instrument_name

    def get_quote_currency(self):
        return self.quote_currency

    def get_base_currency(self):
        return self.base_currency

    def get_price_decimals(self):
        return self.price_decimals

    def get_quantity_decimals(self):
        return self.quantity_decimals

    def get_margin_trading_enabled(self):
        return self.margin_trading_enabled

    def __str__(self):
        result = '{' \
                 + '"instrument_name":"' + self.instrument_name + '",' \
                 + '"quote_currency" :' + str(self.quote_currency) + ',' \
                 + '"base_currency": ' + str(self.base_currency) + ',' \
                 + '"price_decimals": ' + str(self.price_decimals) + ',' \
                 + '"quantity_decimals": ' + str(self.quantity_decimals) + ',' \
                 + '"margin_trading_enabled": ' + str(self.margin_trading_enabled) \
                 + "}"
        return result
