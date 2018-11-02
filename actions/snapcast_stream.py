#!/usr/bin/python3
import logging
from threading import Thread
import snapcast.control
import asyncio
from time import sleep

server_addr='livax.lan'

def run_test(loop):
    return (yield from snapcast.control.create_server(loop, server_addr, reconnect=True))

def start_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    snapserver = loop.run_until_complete(run_test(loop))
    return [loop, snapserver]

def switch_stream(stream_id, duration):
    loop, server = start_server()

    remember_streams = {}

    for group in server.groups:
        remember_streams[group.identifier] = group.stream
        loop.run_until_complete(group.set_stream(stream_id))

    if duration==None:
        return
    logging.info("wait")
    sleep(duration)

    for group in server.groups:
        loop.run_until_complete(group.set_stream(remember_streams[group.identifier]))

class nwThread(Thread):
    def __init__(self, args):
        Thread.__init__(self)
        self.args = args

    def run(self):
        l = self.args.find(" ")
        duration = None
        stream_id = self.args
        if l!=-1:
            duration = int(self.args[l+1:])
            stream_id = self.args[:l]

        switch_stream(stream_id, duration)

def main(args):
    """
    Args: StreamID[ Duration]

    StreamID: registered stream at server
    Duration: in s of the switch
    """
    t = nwThread(args)
    t.start()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main('DoorBell 2')
    logging.debug("done")
