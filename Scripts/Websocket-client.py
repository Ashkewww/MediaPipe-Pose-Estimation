
import asyncio
from websockets.sync.client import connect

def hello():
    with connect("ws://localhost:8765") as websocket:
        websocket.send("Client 2")
        while True:
            message = websocket.recv()
            print(message)
            asyncio.wait(1/15)
        

hello()