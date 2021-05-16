import os
import sys
import time

from db_client.create_connection import create_connection
from db_client.create_sql_insert_variation import create_sql_insert_variation
from db_client.execute_query import execute_query
from db_client.select_query import select_query
from utils.variation_utils import calculate_variation_amount
from utils.variation_utils import print_variation_with_colorama


def main():
    start = time.time()
    database = "/Users/marcoguastalli/opt/sqlite/prices.sqlite"

    conn = create_connection(database)
    try:
        if conn is not None:
            # init
            drop_variation_table(conn)
            create_variation_table(conn)
            calculate_variations(conn)
            # commit
            conn.commit()
            print('calculate execution time: ', time.time() - start, 'seconds')
        else:
            print("Error Connection to DDBB")
    finally:
        if conn is not None:
            conn.close()


def calculate_variations(conn):
    # init flow-control-variables
    source_from = -1
    instrument_from = -1
    amount_from = -1
    # read prices
    query_select = "SELECT amount, source, instrument, created from prices order by source, instrument, created ASC"
    rows = select_query(conn, query_select)
    if rows is not None:
        for row in rows:
            if amount_from == -1:
                # first tuple
                amount_from = row[0]
                source_from = row[1]
                instrument_from = row[2]
            # current tuple
            amount_to = row[0]
            source = row[1]
            instrument = row[2]
            created = row[3]
            # variation is calculated only when source and instrument coincidono
            if source_from == source:
                if instrument_from == instrument:
                    variation = calculate_variation_amount(amount_from, amount_to)
                    if variation is not None:
                        sql_insert_variation = create_sql_insert_variation(source, instrument, variation)
                        execute_query(conn, sql_insert_variation)
                        # print(f"the variation of price for {instrument} is {variation}")
                        print_variation_with_colorama(created, instrument, variation)
                        # set flow-control-variables with current tuple value
                        amount_from = amount_to
                else:
                    # insert the first zero variation for the new instrument
                    sql_insert_variation = create_sql_insert_variation(source, instrument, 0)
                    execute_query(conn, sql_insert_variation)
                    amount_from = row[0]
            else:
                # insert the first zero variation for the new source
                sql_insert_variation = create_sql_insert_variation(source, instrument, 0)
                execute_query(conn, sql_insert_variation)
                amount_from = row[0]
            # set flow-control-variables with current tuple value
            source_from = source
            instrument_from = instrument


def drop_variation_table(conn):
    execute_query(conn, "DROP TABLE IF EXISTS variation")
    conn.commit()


def create_variation_table(conn):
    sql_create_table = '''CREATE TABLE IF NOT EXISTS variation
                                         (id integer PRIMARY KEY AUTOINCREMENT,
                                         source text NOT NULL,
                                         instrument text NOT NULL,
                                         variation REAL NOT NULL DEFAULT 0,
                                         created TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)'''
    execute_query(conn, sql_create_table)
    conn.commit()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Process Interrupted!')
        try:
            sys.exit(0)
        except SystemExit:
            os.error()
