import websockets
import json

class protocol_client(object):

    def __init__(self):
        def noop():
            pass
        self.callback = noop

    def set_message_handler(self, handler):
        self.callback = handler

    async def start(self):
        uri = "wss://ersrealtime.com"
        async with websockets.connect(uri) as websocket:
            await websocket.send(json.dumps(["subscribe", "jameslay:test"]))
            while True:
                rsp = await websocket.recv()
                foldername, topic, payloadstr = rsp.split(":")
                notification = {
                        "foldername": foldername,
                        "topic": topic,
                        "payload": int(payloadstr),
                        }
                self.callback(notification)
                #try:
                #except Exception as e:
                #    print(f"error: {e}")

