#!/bin/python3
import asyncio
from protocol_client import protocol_client

# TODO - disconnect pclient when object realtime client is destroyed

class ers_realtime_client(object):
    def __init__(self):
        self.pclient = protocol_client()
        self.pclient.set_message_handler((lambda notification: self.handle_notification(notification)))
        self.channels = {}

    async def start(self):
        await self.pclient.start()

    def handle_notification(self, notification):
        foldername = notification["foldername"]
        topic = notification["topic"]
        payload = notification["payload"]
        channel = f"{foldername}:{topic}"
        if channel in self.channels == True:
            for listener in self.channels[channel]:
                listener(payload)

    def subscribe(self, foldername, topic, listener):
        channel = f"{foldername}:{topic}"
        if channel in self.channels:
            self.channels[channel].add(listener)
        else:
            self.channels[channel] = {listener}

    def unsubscribe(self, foldername, topic, listener):
        channel = f"{foldername}:{topic}"
        if channel in self.channels:
            self.channels[channel].remove(listener)
            if len(self.channels[channel]) == 0:
                del self.channels[channel]


async def test():
    loop = asyncio.get_event_loop()
    def log_test(payload):
        print(f"received payload {payload}")
    erc = ers_realtime_client()
    task = loop.create_task(erc.start())
    print("subscribing to jameslay:test")
    erc.subscribe("jameslay", "test", log_test)
    print("sleeping for 5 seconds")
    await asyncio.sleep(5)
    print("unsubscribing from jameslay:test")
    erc.unsubscribe("jameslay", "test", log_test)
    print("unsubscribed")
    await task

print("running test")
asyncio.run(test())
print("ran test")
