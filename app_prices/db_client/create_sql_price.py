def create_sql_price(source: str, instrument: str, amount):
    return f"INSERT INTO prices (source, instrument, amount) VALUES ('{source}', '{instrument}', {amount})"
