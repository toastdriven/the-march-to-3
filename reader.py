from __future__ import unicode_literals
import re
from lxml import etree
import six


class RSSFeed(six.Iterator):
    def __init__(self, rss_filename):
        self.rss_filename = rss_filename
        self._loaded = False
        self._raw_content = u''
        self._articles = []
        self._offset = 0

    def strip_tags(self, html):
        # Ugh. Because Bleach isn't ported.
        return re.sub(r'<.*?>', '', html)

    def read(self):
        # Hooray context managers!
        with open(self.rss_filename, u'r') as the_file:
            self._raw_content = the_file.read()

        # Load it.
        # DON'T DO THIS, USE FEEDPARSER INSTEAD, DAMMIT!
        if isinstance(self._raw_content, six.text_type):
            # Only on Py3 do we have to encode this as ASCII.
            self._raw_content = self._raw_content.encode('utf-8')

        root = etree.fromstring(self._raw_content)

        # Parse.
        for item in root.findall(u'.//item'):
            article = {
                u'title': item.find(u'title').text,
                u'link': item.find(u'link').text,
                u'description': self.strip_tags(item.find(u'description').text),
            }
            self._articles.append(article)

        self._loaded = True

    def __iter__(self):
        return self

    def __next__(self):
        if not self._loaded:
            self.read()

        if self._offset > len(self._articles) - 1:
            raise StopIteration()

        article = self._articles[self._offset]
        self._offset += 1
        return article
