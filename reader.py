import bleach
from lxml import etree


class RSSFeed(object):
    def __init__(self, rss_filename):
        self.rss_filename = rss_filename
        self._loaded = False
        self._raw_content = ''
        self._articles = []
        self._offset = 0

    def read(self):
        the_file = open(self.rss_filename, 'r')
        self._raw_content = the_file.read()
        # NO CLOSE MAKES THE INTERPRETER SAD BUT WE'RE ALL GUILTY

        # Load it.
        # DON'T DO THIS, USE FEEDPARSER INSTEAD, DAMMIT!
        root = etree.fromstring(self._raw_content)

        # Parse.
        for item in root.findall('.//item'):
            article = {
                'title': item.find('title').text,
                'link': item.find('link').text,
                'description': bleach.clean(item.find('description').text, strip=True),
            }
            self._articles.append(article)

        self._loaded = True

    def __iter__(self):
        return self

    def next(self):
        if not self._loaded:
            self.read()

        if self._offset > len(self._articles) - 1:
            raise StopIteration()

        article = self._articles[self._offset]
        self._offset += 1
        return article
