import socket, logging
from threading import Thread
from time import sleep
"""
uses a socket to adjust my GLOBO lamp.
Shows how to use the actions folder.
"""

def set_lamp(brightness, redval):
    """
    Adjust lamp to certain color and brightness
    """

    code = (brightness*16+redval).to_bytes(1, byteorder="big")
    try:
        buz = socket.socket()
        buz.connect(('127.0.0.1', 1337))
        logging.debug("send %r"%(code,))
        buz.send(code)
        buz.close()
    except Exception:
        logging.exception("send error")

class dimThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):

        set_lamp(1,15)

        #brigten every min
        for l in range(2,15):
            sleep(59)
            set_lamp(l,15)

        #now get colder
        for r in range(1,15):
            sleep(20)
            set_lamp(15,15-r)

def main(args):
    t = dimThread()
    t.start()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main("")
