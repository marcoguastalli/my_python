from datetime import datetime


def create_sql_insert_variation(source: str, instrument: str, variation):
    created = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    return f"INSERT INTO variation (source, instrument, variation, created) VALUES ('{source}', '{instrument}', {variation}, '{created}')"
