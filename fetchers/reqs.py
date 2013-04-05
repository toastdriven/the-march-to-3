from __future__ import print_function
from __future__ import unicode_literals
import requests
from .exceptions import NotFound


class NewShiny(object):
    def __init__(self):
        super(NewShiny, self).__init__()
        print(u"We love you, Kenneth Reitz! <3")
        print()
        print()

    def fetch(self, url):
        resp = requests.get(url)

        if int(resp.status_code) != 200:
            raise NotFound(url)

        return resp.text
