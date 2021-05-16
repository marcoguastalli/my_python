class Price:
    def __init__(self, source, instrument, price_from, price_to, variation, created, updated):
        self.source = source
        self.instrument = instrument
        self.price_from = price_from
        self.price_to = price_to
        self.variation = variation
        self.created = created
        self.updated = updated

    def get_source(self):
        return self.source

    def get_instrument(self):
        return self.instrument

    def get_price_from(self):
        return self.price_from

    def get_price_to(self):
        return self.price_to

    def get_variation(self):
        return self.variation

    def get_created(self):
        return self.created

    def get_updated(self):
        return self.updated

    # return the key for the dictionary
    def get_key(self):
        return self.source + "_" + self.instrument

    def __str__(self):
        result = '{' + '"source":"' + self.source + '",' \
                 + '"instrument":"' + self.instrument + '",' \
                 + '"price_from":"' + str(self.price_from) + '",' \
                 + '"price_to":"' + str(self.price_to) + '",' \
                 + '"variation":"' + str(self.variation) + '",' \
                 + '"created":"' + str(self.created) + '",' \
                 + '"updated":"' + str(self.updated) + '",' \
                 + "}"
        return result
