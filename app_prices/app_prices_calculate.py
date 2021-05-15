import os
import sys
import time

from db_client.create_connection import create_connection
from db_client.create_sql_insert_variation import create_sql_insert_variation
from db_client.execute_query import execute_query
from db_client.select_query import select_query


def main():
    start = time.time()
    database_read = "/Users/marcoguastalli/opt/sqlite/prices.sqlite"
    database_write = "/Users/marcoguastalli/opt/sqlite/calcs.sqlite"

    conn_read = create_connection(database_read)
    conn_write = create_connection(database_write)
    try:
        if conn_read is not None and conn_write is not None:
            # read prices
            source = 'CDC'
            instrument = 'CRO_USDT'
            query_select = f"SELECT amount from prices where source = '{source}' and instrument = '{instrument}' order by created"
            rows = select_query(conn_read, query_select)
            amount_from = -1
            if rows is not None:
                for row in rows:
                    if amount_from == -1:
                        amount_from = row[0]
                    amount_to = row[0]
                    variation = calculate_variation(amount_from, amount_to)
                    sql_insert_variation = create_sql_insert_variation(source, instrument, variation)
                    execute_query(conn_write, sql_insert_variation)

            # commit
            conn_write.commit()
            print('calculate execution time: ', time.time() - start, 'seconds')
        else:
            print("Error Connection to DDBB")
    finally:
        if conn_read is not None:
            conn_read.close()
        if conn_write is not None:
            conn_write.close()


def calculate_variation(amount_from, amount_to):
    print(f"amount from: {amount_from}")
    print(f"amount   to: {amount_to}")
    variation = ((amount_to * amount_from) / amount_from) * 100
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
