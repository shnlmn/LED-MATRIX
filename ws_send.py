import websockets
import asyncio

async def update():
    async with websockets.connect("ws://192.168.254.79:5555") as websocket:
        await websocket.send("red_bright:150")
        await websocket.recv()

asyncio.get_event_loop().run_until_complete(update())
