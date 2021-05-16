import asyncio
import os
import sys
import time

import aioschedule as schedule

from api_client.get_ticker import GetTicker
from db_client.create_connection import create_connection
from db_client.create_sql_insert_price import create_sql_insert_price
from db_client.create_sql_insert_variation import create_sql_insert_variation
from db_client.execute_query import execute_query
from db_client.select_query import select_query
from utils.variation_utils import calculate_variation_amount
from utils.variation_utils import print_variation_with_colorama


async def main():
    start = time.time()
    database = "/Users/marcoguastalli/opt/sqlite/prices.sqlite"

    conn = create_connection(database)
    try:
        if conn is not None:
            # call CDC API
            await create_prices_from_api(conn)
            conn.commit()
            # process prices
            await calculate_variations(conn)
            conn.commit()
            # clean for next run
            #await clean_table_price(conn)
            conn.commit()
            print('execution time: ', time.time() - start, 'seconds')
        else:
            print("Error Connection to DDBB:" + database)
    finally:
        if conn is not None:
            conn.close()


async def create_prices_from_api(conn):
    # call CDC API
    ticker = GetTicker('https://api.crypto.com/v2/public/get-ticker')
    response = ticker.do_get()
    tickers_list = response.json()['result']['data']
    # insert the instrument-name and the price of the latest trade
    for ticker in tickers_list:
        query_insert = create_sql_insert_price('CDC', ticker['i'], ticker['a'])
        execute_query(conn, query_insert)


async def calculate_variations(conn):
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


async def clean_table_price(conn):
    execute_query(conn, "DELETE FROM prices")


if __name__ == '__main__':
    try:
        schedule.every(1).seconds.do(main)
        loop = asyncio.get_event_loop()
        while True:
            loop.run_until_complete(schedule.run_pending())
            time.sleep(1)
    except KeyboardInterrupt:
        print('Process Interrupted!')
        try:
            sys.exit(0)
        except SystemExit:
            os.error()
