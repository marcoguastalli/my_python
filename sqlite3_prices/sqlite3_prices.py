import os
import sys

from create_connection import create_connection
from execute_query import execute_query


def main():
    database = "/Users/marcoguastalli/opt/sqlite/prices.sqlite"

    conn = create_connection(database)
    try:
        if conn is not None:
            # drop table
            # sql_drop_table = "DROP TABLE prices"
            # execute_query(conn, sql_drop_table)
            # conn.commit()
            # create table
            sql_create_table = '''CREATE TABLE IF NOT EXISTS prices
                                         (id integer PRIMARY KEY AUTOINCREMENT,
                                         source text NOT NULL,
                                         symbol text NOT NULL,
                                         amount REAL NOT NULL DEFAULT 0,
                                         created TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)'''
            execute_query(conn, sql_create_table)
            conn.commit()
            # first insert
            query_insert = "INSERT INTO prices VALUES (1, 'BIN', 'BTC_USDC', 55880.38, CURRENT_TIMESTAMP)"
            execute_query(conn, query_insert)
            query_insert = "INSERT INTO prices (source, symbol, amount) VALUES ('CDC', 'BTC_USDC', 55999.99)"
            execute_query(conn, query_insert)
            conn.commit()
            # select
            query_select = "SELECT * FROM prices ORDER BY created DESC"
            cursor = conn.cursor()
            for row in cursor.execute(query_select):
                print(row)
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
