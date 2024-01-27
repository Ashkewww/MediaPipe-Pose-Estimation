
import pprint as p
import asyncio, json
from websockets.sync.client import connect

def hello():
    with connect("ws://localhost:6969") as websocket:
        while True:
            message = json.loads(websocket.recv())
            if message['status'] == 'Failure':
                print("Person not found")
            else:
                print("Data is being recieved")
            asyncio.wait(1/15)
        

if __name__ == "__main__":
    try:
        hello()
    except KeyboardInterrupt:
        print("LOG::Disconnected from the server")