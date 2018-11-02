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
    def __init__(self, args):
        Thread.__init__(self)
        self.args = args

    def run(self):
        l = self.args.find(" ")
        shine = self.args
        cool = self.args
        if l!=-1:
            cool = self.args[l+1:]
            shine = self.args[:l]
        
        shine = int(shine)
        cool = int(cool)

        set_lamp(1,15)

        #brigten every min
        for l in range(2,15):
            sleep(shine)
            set_lamp(l,15)

        #now get colder
        for r in range(1,15):
            sleep(cool)
            set_lamp(15,15-r)

def main(args):
    """
    Args: rise cool

    rise: delay between a step while rising
    cool: delay between a step of cooling (after rise is done)
    """
    t = dimThread(args)
    t.start()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main("2 1")
