class Price:
    def __init__(self, source, instrument, amount, created):
        self.source = source
        self.instrument = instrument
        self.amount = amount
        self.created = created

    def get_source(self):
        return self.source

    def get_instrument(self):
        return self.instrument

    def get_amount(self):
        return self.amount

    def get_created(self):
        return self.created

    def __str__(self):
        result = '{' + '"source":"' + self.source + '",' + '"instrument":"' + self.instrument + '",' + '"amount":"' + str(self.amount) + '",' + '"created":"' + str(self.created) + '",' + "}"
        return result
