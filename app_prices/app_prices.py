import asyncio
import os
import sys
import time
from datetime import datetime
from colorama import Fore, Style
import aioschedule as schedule

from api_client.get_ticker import GetTicker
from db_client.create_connection import create_connection
from db_client.execute_query import execute_query
from model.price import Price
from utils.variation_utils import calculate_variation_amount
from utils.variation_utils import print_variation_with_colorama


async def main():
    start = time.time()
    database = "/Users/marcoguastalli/opt/sqlite/prices.sqlite"

    conn = create_connection(database)
    try:
        if conn is not None:
            prices_dict = await create_prices_from_api(conn, {})
            conn.commit()
            prices_dict = await create_prices_from_api(conn, prices_dict)
            conn.commit()
            print(Style.RESET_ALL + "execution time: ", time.time() - start, "seconds")
        else:
            print(Fore.RED + "Error Connection to DDBB:" + database)
    finally:
        if conn is not None:
            conn.close()


async def create_prices_from_api(conn, prices_dict):
    source = "CDC"
    # call CDC API
    tickers_list = await get_prices_from_api()
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
            price = Price(source, instrument, price_to, created)
            prices_dict[price.get_key()] = price
        else:
            price_from = price_object_from_dict.get_amount()
            price_to = ticker['a']
            variation = calculate_variation_amount(price_from, price_to)
            if variation is None:
                variation = 0
            updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            query_update = f"UPDATE prices SET price_from={price_from}, price_to={price_to}, variation={variation}, updated='{updated}'" \
                           f" WHERE source='{source}' AND instrument='{instrument}'"
            execute_query(conn, query_update)
            price = Price(source, instrument, price_to, updated)
            prices_dict[price.get_key()] = price

            print_variation_with_colorama(updated, instrument, variation)

    return prices_dict


async def get_prices_from_api():
    ticker = GetTicker('https://api.crypto.com/v2/public/get-ticker')
    response = ticker.do_get()
    tickers_list = response.json()['result']['data']
    return tickers_list


if __name__ == '__main__':
    try:
        schedule.every(2).seconds.do(main)
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
