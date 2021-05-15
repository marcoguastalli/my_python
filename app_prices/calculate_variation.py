import os
import sys
import time

from db_client.create_connection import create_connection
from db_client.create_sql_insert_variation import create_sql_insert_variation
from db_client.execute_query import execute_query
from db_client.select_query import select_query


def calculate_variation():
    start = time.time()
    database = "/Users/marcoguastalli/opt/sqlite/prices.sqlite"

    conn = create_connection(database)
    try:
        if conn is not None:
            # init flow-control-variables
            source_from = -1
            instrument_from = -1
            amount_from = -1
            id_to_delete = []

            # read prices
            query_select = "SELECT amount, source, instrument, id from prices order by source, instrument, created ASC"
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
                    id_to_delete.append(row[3])
                    # variation is calculated only when source and instrument coincidono
                    if source_from == source:
                        if instrument_from == instrument:
                            variation = calculate_variation_amount(amount_from, amount_to)
                            if variation is not None:
                                sql_insert_variation = create_sql_insert_variation(source, instrument, variation)
                                execute_query(conn, sql_insert_variation)
                                print(f"the variation of price for {instrument} is {variation}")
                                if variation >= 1 or variation <= -1:
                                    print(f"WARN! the variation of price for {instrument} is more than {variation}%!")
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
            # the following ids should be deleted
            print(f"DELETE FROM prices WHERE id IN({id_to_delete}")
            # commit
            conn.commit()
            print('calculate execution time: ', time.time() - start, 'seconds')
        else:
            print("Error Connection to DDBB")
    finally:
        if conn is not None:
            conn.close()


def calculate_variation_amount(amount_from, amount_to):
    try:
        variation = ((amount_to - amount_from) / amount_from) * 100
    except ZeroDivisionError:
        return None
    return variation


if __name__ == '__main__':
    try:
        calculate_variation()
    except KeyboardInterrupt:
        print('Process Interrupted!')
        try:
            sys.exit(0)
        except SystemExit:
            os.error()
