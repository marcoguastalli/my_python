from datetime import datetime


def create_sql_insert_price(source: str, instrument: str, amount):
    created = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    return f"INSERT INTO prices (source, instrument, amount, created) VALUES ('{source}', '{instrument}', {amount}, '{created}')"
