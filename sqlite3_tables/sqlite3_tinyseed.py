import os
import sys
from datetime import datetime

from create_connection import create_connection
from execute_query import execute_query


def main():
    database = "/Users/marco27/Downloads/bip39_tinyseed.sqlite"

    conn = create_connection(database)
    try:
        if conn is not None:
            # drop table
            sql_drop_table = "DROP TABLE IF EXISTS bip39_tinyseed"
            execute_query(conn, sql_drop_table)
            conn.commit()
            # create table
            sql_create_table = '''CREATE TABLE IF NOT EXISTS bip39_tinyseed
                                         (id integer PRIMARY KEY,
                                         word text NOT NULL,
                                         i2048 INT NOT NULL DEFAULT 0,
                                         i1024 INT NOT NULL DEFAULT 0,
                                         i512 INT NOT NULL DEFAULT 0,
                                         i256 INT NOT NULL DEFAULT 0,
                                         i128 INT NOT NULL DEFAULT 0,
                                         i56 INT NOT NULL DEFAULT 0,
                                         i32 INT NOT NULL DEFAULT 0,
                                         i16 INT NOT NULL DEFAULT 0,
                                         i8 INT NOT NULL DEFAULT 0,
                                         i4 INT NOT NULL DEFAULT 0,
                                         i2 INT NOT NULL DEFAULT 0,
                                         i1 INT NOT NULL DEFAULT 0)'''
            execute_query(conn, sql_create_table)
            conn.commit()
            # data insert
            query_insert = f"INSERT INTO bip39_tinyseed (id, word, i2048, i1024, i512, i256, i128, i56, i32, i16, i8, i4, i2, i1) VALUES (1, 'abandon', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)"
            execute_query(conn, query_insert)
            query_insert = f"INSERT INTO bip39_tinyseed (id, word, i2048, i1024, i512, i256, i128, i56, i32, i16, i8, i4, i2, i1) VALUES (2, 'ability', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0)"
            execute_query(conn, query_insert)
            query_insert = f"INSERT INTO bip39_tinyseed (id, word, i2048, i1024, i512, i256, i128, i56, i32, i16, i8, i4, i2, i1) VALUES (3, 'able', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1)"
            execute_query(conn, query_insert)
            query_insert = f"INSERT INTO bip39_tinyseed (id, word, i2048, i1024, i512, i256, i128, i56, i32, i16, i8, i4, i2, i1) VALUES (4, 'about', 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0)"
            execute_query(conn, query_insert)
            conn.commit()
            # select
            query_select = "SELECT * FROM bip39_tinyseed ORDER BY id"
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
