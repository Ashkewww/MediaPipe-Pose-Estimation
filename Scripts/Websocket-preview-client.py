
import asyncio
from websockets.sync.client import connect

def hello():
    with connect("ws://localhost:6969") as websocket:
        while True:
            message = websocket.recv()
            print(message)
            asyncio.wait(1/15)
        

hello()