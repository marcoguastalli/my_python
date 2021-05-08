def create_sql_price(source: str, symbol: str, amount):
    return f"INSERT INTO prices (source, symbol, amount) VALUES ('{source}', '{symbol}', {amount})"
