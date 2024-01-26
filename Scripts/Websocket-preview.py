import asyncio
from websockets.server import serve

async def echo(websocket):
    while True:
        await websocket.send(f"Continuous Data working: Message was Recieved")
        await asyncio.sleep(1/15)

async def main():
    async with serve(echo, "localhost", 6969):
        await asyncio.Future()
        
asyncio.run(main())

