from __future__ import print_function
from __future__ import unicode_literals
from reader import RSSFeed
from fetchers import Fetcher

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


my_feeds = {
    # WARNING, WARNING! DANGER WILL ROBINSON!
    # THESE ARE BYTE STRINGS!
    u'Toast Driven': u'http://toastdriven.com/feeds/fresh_news/',
    u'Django': u'https://www.djangoproject.com/rss/weblog/',
}


class RSSFetcher(Fetcher):
    use = u'fetchers.stdlib.OldBroke'
    # use = u'fetchers.reqs.NewShiny'


def fetch():
    rss_filenames = []
    fetcher = RSSFetcher()

    for title, url in my_feeds.items():
        rss_filenames.append(fetcher.fetch(title, url))

    return rss_filenames


def read(rss_filenames):
    for rss_filename in rss_filenames:
        rss = RSSFeed(rss_filename)

        for article in rss:
            yield article


def main():
    rss_filenames = fetch()
    articles = read(rss_filenames)

    for article in articles:
        print(u'"{0}" ({1}): {2}...'.format(
            article[u'title'],
            urlparse(article[u'link']).netloc,
            article.get(u'description', u'')[:25]
        ))


if __name__ == u'__main__':
    main()
