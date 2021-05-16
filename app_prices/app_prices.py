import asyncio
import os
import sys
import time

import aioschedule as schedule

from api_client.get_ticker import GetTicker
from db_client.create_connection import create_connection
from db_client.create_sql_insert_price import create_sql_insert_price
from db_client.execute_query import execute_query


async def main():
    start = time.time()
    database = "/Users/marcoguastalli/opt/sqlite/prices.sqlite"

    conn = create_connection(database)
    try:
        if conn is not None:
            # call CDC API
            ticker = GetTicker('https://api.crypto.com/v2/public/get-ticker')
            response = ticker.do_get()
            tickers_list = response.json()['result']['data']
            # insert the instrument-name and the price of the latest trade
            for ticker in tickers_list:
                query_insert = create_sql_insert_price('CDC', ticker['i'], ticker['a'])
                execute_query(conn, query_insert)

            # commit
            conn.commit()
            print('prices inserted in ', time.time() - start, 'seconds')
        else:
            print("Error Connection to DDBB:" + database)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    try:
        # schedule.every().minute.do(main)
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
