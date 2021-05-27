import os
import sys

from db_client.create_connection import create_connection
from db_client.execute_query import execute_query


def main():
    database = "/Users/marcoguastalli/opt/sqlite/prices.sqlite"

    conn = create_connection(database)
    try:
        if conn is not None:
            # drop tables
            execute_query(conn, "DROP TABLE IF EXISTS prices")
            conn.commit()
            # create table
            sql_create_table = '''CREATE TABLE IF NOT EXISTS prices (
                                         id INTEGER PRIMARY KEY,
                                         source TEXT NOT NULL,
                                         instrument TEXT NOT NULL,
                                         price_from REAL NOT NULL DEFAULT 0,
                                         price_to REAL NOT NULL DEFAULT 0,
                                         variation REAL NOT NULL DEFAULT 0,
                                         created TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                         updated TEXT NOT NULL DEFAULT "")'''
            execute_query(conn, sql_create_table)
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
