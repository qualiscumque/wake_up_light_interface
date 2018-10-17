import logging
from requests import get
from xml.etree.ElementTree import fromstring as parseXML
from threading import Thread
from dlnap.dlnap import discover # from https://github.com/cherezov/dlnap
"""
Grab the newest Episode of a podcast and send it to a DLNA Device
"""

DLNA_DEVICE = '10.168.0.207'

def getLastRssFeedEntry(uri):
    r = get(uri)
    if r.status_code != 200:
        logging.info("Not a successfull request.")
        return None
    
    root = parseXML(r.text)
    # rss > channel[0] > item[0] > enclosure[]
    for item in root.find('channel').find('item').findall('enclosure'):
        if item.get('type') == 'audio/mp3':
            return item.get('url')

    logging.info("No mp3 enclosure found")
    return None

def playViaDLNA(ip, url, vol):
    allDevices = discover(ip=ip, timeout=10)
    if not allDevices:
        logging.info('No compatible devices found.')
        return
    d = allDevices[0]
    d.stop()
    d.set_current_media(url=url)
    d.volume(vol)
    d.play()


class nwThread(Thread):
    def __init__(self, url):
        Thread.__init__(self)
        self.url = url

    def run(self):
        mp3uri = getLastRssFeedEntry(self.url)
        if mp3uri:
            logging.info(mp3uri)
            playViaDLNA(DLNA_DEVICE, mp3uri, 20)

def main(url):
    """
    Args: url

    url: of podcast
    """
    t = nwThread(url)
    t.start()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main('http://www.tagesschau.de/export/podcast/tagesschau/')
