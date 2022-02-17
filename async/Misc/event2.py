#!/usr/bin/micropython

import time
import uasyncio as asyncio
from uasyncio import Event


async def waiter(event):
    print('waiting for it ...')
    await event.wait()
    print('... got it!')

    #async with event: Error
    #    print('... got it 2!')

async def main():
    # Create an Event object.
    event = asyncio.Event()

    # Spawn a Task to wait until 'event' is set.
    waiter_task = asyncio.create_task(waiter(event))

    #print('time.sleep(2) A')
    #time.sleep(2)

    # Sleep for 1 second and set the event.
    print('A sleep 3')
    await asyncio.sleep(3)
    event.set()

    #print('time.sleep(2) B')
    #time.sleep(2)

    # Wait until the waiter task is finished.
    await waiter_task



asyncio.run(main())
