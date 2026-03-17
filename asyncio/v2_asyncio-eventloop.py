import asyncio
import time

import aioschedule as schedule


async def main():
    print('Hello ...')
    await asyncio.sleep(1)
    print('... World!')


schedule.every().hour.at(":27").do(main)

loop = asyncio.get_event_loop()

while True:
    loop.run_until_complete(schedule.run_pending())
    time.sleep(1)
