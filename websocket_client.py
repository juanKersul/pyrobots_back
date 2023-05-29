import websockets
import asyncio


async def listen():
    async with websockets.connect("ws://localhost:8765") as ws:
        while True:
            message = await ws.recv()
            print(message)


asyncio.get_event_loop().run_until_complete(listen())
