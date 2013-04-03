import requests
from .exceptions import NotFound


class NewShiny(object):
    def __init__(self):
        super(NewShiny, self).__init__()
        print "We love you, Kenneth Reitz! <3"
        print
        print

    def fetch(self, url):
        resp = requests.get(url)

        if int(resp.status_code) != 200:
            raise NotFound(url)

        return resp.text
