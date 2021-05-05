import os
import sys

from create_connection import create_connection
from execute_query import execute_query


def main():
    database = "/Users/marcoguastalli/opt/sqlite/my_python_prices.sqlite"

    sql_create_stocks_table = '''CREATE TABLE IF NOT EXISTS prices
                                (id integer PRIMARY KEY
                                symbol text NOT NULL, 
                                amount real NOT NULL, 
                                created text NOT NULL)'''

    conn = create_connection(database)
    try:
        if conn is not None:
            # create table
            execute_query(conn, sql_create_stocks_table)
            conn.commit()
            # first insert
            query_insert = "INSERT INTO prices VALUES (1, 'BTC', 48000.14, '2021-05-05')"
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
