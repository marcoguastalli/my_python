import os
import sys
from datetime import datetime

from create_connection import create_connection
from execute_query import execute_query


def main():
    database = "/Users/marcoguastalli/opt/sqlite/variation.sqlite"

    conn = create_connection(database)
    try:
        if conn is not None:
            # drop table
            sql_drop_table = "DROP TABLE variation"
            execute_query(conn, sql_drop_table)
            conn.commit()
            # create table
            sql_create_table = '''CREATE TABLE IF NOT EXISTS variation
                                         (id integer PRIMARY KEY AUTOINCREMENT,
                                         source text NOT NULL,
                                         instrument text NOT NULL,
                                         variation REAL NOT NULL DEFAULT 0,
                                         created TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)'''
            execute_query(conn, sql_create_table)
            conn.commit()
            # data insert
            created = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            query_insert = f"INSERT INTO variation (source, instrument, amount, created) VALUES ('TEST', 'BTC_USDC', -27, '{created}')"
            execute_query(conn, query_insert)
            conn.commit()
            # select
            query_select = "SELECT * FROM variation ORDER BY created DESC"
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
