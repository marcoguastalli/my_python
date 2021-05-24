import asyncio
import os
import sys
import time
from datetime import datetime

import aioschedule as schedule
from colorama import Fore, Style

from bnc_api_client.get_ticker import GetTicker as BncGetTicker
from cdc_api_client.get_ticker import GetTicker as CdcGetTicker
from db_client.create_connection import create_connection
from db_client.execute_query import execute_query
from db_client.select_query import select_query
from model.price import Price
from utils.variation_utils import calculate_variation_amount
from utils.variation_utils import print_variation_with_colorama


async def main():
    start = time.time()
    database = "/Users/marcoguastalli/opt/sqlite/prices.sqlite"

    conn = create_connection(database)
    try:
        if conn is not None:
            prices_dict = {}

            # read SQLite table 'prices' and create a dictionary with Price object
            price_table_rows = select_query(conn, "SELECT source, instrument, price_from, price_to, variation, created, updated"
                                                  "  FROM prices"
                                                  " ORDER BY source, instrument, created ASC")
            if price_table_rows is not None:
                for row in price_table_rows:
                    price = Price(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                    prices_dict[price.get_key()] = price

            # call BNC API and update the dictionary with Price object
            await create_prices_from_bnc_api(conn, prices_dict)

            # call CDC API and update the dictionary with Price object
            await create_prices_from_cdc_api(conn, prices_dict)

            # log time
            print(Style.RESET_ALL + "At " + datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + " the process end in: ", time.time() - start, "seconds")
        else:
            print(Fore.RED + "Error Connection to DDBB:" + database)
    finally:
        if conn is not None:
            conn.close()


async def create_prices_from_bnc_api(conn, prices_dict):
    source = "BNC"
    # call BCN API
    tickers_list = await get_prices_from_bnc_api()
    # insert the instrument-name and the price of the latest trade
    for ticker in tickers_list:
        instrument = ticker['symbol']
        price_key = source + "_" + instrument
        price_object_from_dict = prices_dict.get(price_key)
        if price_object_from_dict is None:
            # first loop
            price_from = float(ticker['lastPrice'])
            price_to = float(ticker['lastPrice'])
            variation = 0
            created = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            query_insert = f"INSERT INTO prices (source, instrument, price_from, price_to, variation, created) " \
                           f"VALUES ('{source}', '{instrument}', {price_from}, {price_to}, {variation}, '{created}')"
            execute_query(conn, query_insert)
        else:
            price_from = price_object_from_dict.get_price_from()
            price_to = float(ticker['lastPrice'])
            variation = calculate_variation_amount(price_from, price_to)
            if variation is None:
                variation = 0
            updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            query_update = f"UPDATE prices SET price_from={price_from}, price_to={price_to}, variation={variation}, updated='{updated}'" \
                           f" WHERE source='{source}' AND instrument='{instrument}'"
            execute_query(conn, query_update)
            # log variation
            print_variation_with_colorama(updated, instrument, variation)
    # commit
    conn.commit()
    pass


async def create_prices_from_cdc_api(conn, prices_dict):
    source = "CDC"
    # call CDC API
    tickers_list = await get_prices_from_cdc_api()
    # insert the instrument-name and the price of the latest trade
    for ticker in tickers_list:
        instrument = ticker['i']
        price_key = source + "_" + instrument
        price_object_from_dict = prices_dict.get(price_key)
        if price_object_from_dict is None:
            # first loop
            price_from = ticker['a']
            price_to = ticker['a']
            variation = 0
            created = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            query_insert = f"INSERT INTO prices (source, instrument, price_from, price_to, variation, created) " \
                           f"VALUES ('{source}', '{instrument}', {price_from}, {price_to}, {variation}, '{created}')"
            execute_query(conn, query_insert)
        else:
            price_from = price_object_from_dict.get_price_from()
            price_to = ticker['a']
            variation = calculate_variation_amount(price_from, price_to)
            if variation is None:
                variation = 0
            updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            query_update = f"UPDATE prices SET price_from={price_from}, price_to={price_to}, variation={variation}, updated='{updated}'" \
                           f" WHERE source='{source}' AND instrument='{instrument}'"
            execute_query(conn, query_update)
            # log variation
            print_variation_with_colorama(updated, instrument, variation)
    # commit
    conn.commit()
    pass


async def get_prices_from_bnc_api():
    ticker = BncGetTicker('https://api.binance.com/api/v3/ticker/24hr')
    response = ticker.do_get()
    tickers_list = response.json()
    return tickers_list


async def get_prices_from_cdc_api():
    ticker = CdcGetTicker('https://api.crypto.com/v2/public/get-ticker')
    response = ticker.do_get()
    tickers_list = response.json()['result']['data']
    return tickers_list


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
