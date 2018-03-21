#!/usr/bin/env python

import asyncio
import datetime
import random
import websockets
import socket

async def time(websocket, path):
    name = await websocket.recv()
    print("< {}".format(name))


start_server = websockets.serve(time, '127.0.0.1', 5555)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
