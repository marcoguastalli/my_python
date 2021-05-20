import asyncio
import hashlib
import hmac
import os
import sqlite3
import sys
import time
from datetime import datetime

import aioschedule as schedule
import requests
from colorama import Fore, Style


class ApiRequest:
    def __init__(self, url, api_key, secret_key):
        self.url = url
        self.api_key = api_key
        self.secret_key = secret_key

    @staticmethod
    def get_nonce():
        return int(time.time() * 1000)

    def sign_request(self, req):
        return sign_request(req, self.api_key, self.secret_key)


class GetTicker(ApiRequest):
    def __init__(self, url):
        super().__init__(url, None, None)

    def do_get(self):
        response = None
        try:
            headers = {'Content-type': 'application/json'}
            response = requests.get(self.url, headers=headers)

        except Exception as e:
            print("Error get-ticker")
            print(e)

        return response


def sign_request(req, api_key, secret_key):
    if req is None or api_key is None or secret_key is None:
        return None
    # First ensure the params are alphabetically sorted by key
    param_string = ''
    if 'params' in req:
        for key in sorted(req['params']):
            param_string += key
            param_string += str(req['params'][key])
    # Combine method + id + api_key + parameter string + nonce
    sig_pay_load = req['method'] + str(req['id']) + req['api_key'] + param_string + str(req['nonce'])
    # Use HMAC-SHA256 to hash the above using the API Secret as the cryptographic key
    req['api_key'] = api_key
    req['sig'] = hmac.new(bytes(str(secret_key), 'utf-8'), msg=bytes(sig_pay_load, 'utf-8'), digestmod=hashlib.sha256).hexdigest()
    # Encode the output as a hex string
    return req


class Price:
    def __init__(self, source, instrument, price_from, price_to, variation, created, updated):
        self.source = source
        self.instrument = instrument
        self.price_from = price_from
        self.price_to = price_to
        self.variation = variation
        self.created = created
        self.updated = updated

    def get_source(self):
        return self.source

    def get_instrument(self):
        return self.instrument

    def get_price_from(self):
        return self.price_from

    def get_price_to(self):
        return self.price_to

    def get_variation(self):
        return self.variation

    def get_created(self):
        return self.created

    def get_updated(self):
        return self.updated

    # return the key for the dictionary
    def get_key(self):
        return self.source + "_" + self.instrument

    def __str__(self):
        result = '{' + '"source":"' + self.source + '",' + '"instrument":"' + self.instrument + '",' + '"price_from":"' + str(self.price_from) + '",' + '"price_to":"' + str(self.price_to) + '",' + '"variation":"' + str(self.variation) + '",' + '"created":"' + str(self.created) + '",' + '"updated":"' + str(self.updated) + '",' + "}"
        return result


async def main():
    start = time.time()
    conn = sqlite3.connect("prices.sqlite")
    try:
        if conn is not None:
            prices_dict = {}

            # read SQLite table 'prices' and create a dictionary with Price object
            cur = conn.cursor()
            cur.execute("SELECT source, instrument, price_from, price_to, variation, created, updated"
                        "  FROM prices"
                        " ORDER BY source, instrument, created ASC")
            price_table_rows = cur.fetchall()
            if price_table_rows is not None:
                for row in price_table_rows:
                    price = Price(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                    prices_dict[price.get_key()] = price

            # call CDC API and update the dictionary with Price object
            await create_prices_from_api(conn, prices_dict)

            # log time
            print(Style.RESET_ALL + "At " + datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + " the process end in: ", time.time() - start, "seconds")
        else:
            print(Fore.RED + "Error Connection to DDBB.")
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
            cursor = conn.cursor()
            cursor.execute(query_insert)
        else:
            price_from = price_object_from_dict.get_price_from()
            price_to = ticker['a']
            variation = calculate_variation_amount(price_from, price_to)
            if variation is None:
                variation = 0
            updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            query_update = f"UPDATE prices SET price_from={price_from}, price_to={price_to}, variation={variation}, updated='{updated}'" \
                           f" WHERE source='{source}' AND instrument='{instrument}'"
            cursor = conn.cursor()
            cursor.execute(query_update)
            # log variation
            print_variation_with_colorama(updated, instrument, variation)
    # commit
    conn.commit()
    pass


async def get_prices_from_api():
    ticker = GetTicker('https://api.crypto.com/v2/public/get-ticker')
    response = ticker.do_get()
    tickers_list = response.json()['result']['data']
    return tickers_list


def calculate_variation_amount(amount_from, amount_to):
    try:
        variation = ((amount_to - amount_from) / amount_from) * 100
    except ZeroDivisionError:
        return None
    return variation


def print_variation_with_colorama(created, instrument, variation):
    if variation is None:
        return
    if variation >= 2:
        print(Fore.LIGHTGREEN_EX + f"WARN! the variation of price for {instrument} is more than {variation}% at {created}!")
    elif variation >= 1.5:
        print(Fore.GREEN + f"WARN! the variation of price for {instrument} is more than {variation}% at {created}!")
    elif variation >= 1:
        print(Style.RESET_ALL + f"WARN! the variation of price for {instrument} is more than {variation}% at {created}!")
    elif variation <= -1:
        print(Style.RESET_ALL + f"WARN! the variation of price for {instrument} is more than {variation}% at {created}!")
    elif variation <= -2:
        print(Fore.LIGHTRED_EX + f"WARN! the variation of price for {instrument} is more than {variation}% at {created}!")


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
