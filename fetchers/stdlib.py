from __future__ import unicode_literals
from .exceptions import NotFound

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen


class OldBroke(object):
    def fetch(self, url):
        handler = urlopen(url)

        if int(handler.getcode()) != 200:
            raise NotFound(url)

        return handler.read().decode('utf-8')
