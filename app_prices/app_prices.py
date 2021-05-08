import os
import sys

from api_client.get_ticker import GetTicker
from db_client.create_connection import create_connection
from db_client.create_sql_price import create_sql_price
from db_client.execute_query import execute_query


def main():
    database = "/Users/marcoguastalli/opt/sqlite/prices.sqlite"

    conn = create_connection(database)
    try:
        if conn is not None:
            # call CDC API
            ticker = GetTicker('https://api.crypto.com/v2/public/get-ticker')
            response = ticker.do_get()
            tickers_list = response.json()['result']['data']
            # insert the instrument-name and the price of the latest trade
            for ticker in tickers_list:
                query_insert = create_sql_price('CDC', ticker['i'], ticker['a'])
                execute_query(conn, query_insert)

            # commit
            conn.commit()

        else:
            print("Error Connection to DDBB:" + database)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os.error()
