import urllib2
from .exceptions import NotFound


class OldBroke(object):
    def fetch(self, url):
        req = urllib2.Request(url)
        handler = urllib2.urlopen(req)

        if int(handler.getcode()) != 200:
            raise NotFound(url)

        return handler.read()
