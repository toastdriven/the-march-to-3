import requests
from .exceptions import NotFound


class NewShiny(object):
    def fetch(self, url):
        resp = requests.get(url)

        if int(resp.status_code) != 200:
            raise NotFound(url)

        return resp.text
