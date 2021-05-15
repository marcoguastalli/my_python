import os
import sys
import time

from db_client.create_connection import create_connection
from db_client.create_sql_insert_variation import create_sql_insert_variation
from db_client.execute_query import execute_query
from db_client.select_query import select_query


def main():
    start = time.time()
    database = "/Users/marcoguastalli/opt/sqlite/prices.sqlite"

    conn = create_connection(database)
    try:
        if conn is not None:
            # read prices
            source = 'TEST'
            instrument = 'BTC_USDC'
            query_select = f"SELECT amount from prices where source = '{source}' and instrument = '{instrument}' order by created"
            rows = select_query(conn, query_select)
            amount_from = -1
            if rows is not None:
                for row in rows:
                    if amount_from == -1:
                        amount_from = row[0]
                    amount_to = row[0]
                    variation = calculate_variation(amount_from, amount_to)
                    if variation is not None:
                        sql_insert_variation = create_sql_insert_variation(source, instrument, variation)
                        execute_query(conn, sql_insert_variation)

            # commit
            conn.commit()
            print('calculate execution time: ', time.time() - start, 'seconds')
        else:
            print("Error Connection to DDBB")
    finally:
        if conn is not None:
            conn.close()


def calculate_variation(amount_from, amount_to):
    print(f"amount from: {amount_from}")
    print(f"amount   to: {amount_to}")
    try:
        variation = ((amount_to - amount_from) / amount_from) * 100
    except ZeroDivisionError:
        return None
    print(f"variation  : {variation}")
    print("")
    return variation


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Process Interrupted!')
        try:
            sys.exit(0)
        except SystemExit:
            os.error()
