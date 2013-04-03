import urlparse
from reader import RSSFeed
from fetchers import Fetcher


my_feeds = {
    # WARNING, WARNING! DANGER WILL ROBINSON!
    # THESE ARE BYTE STRINGS!
    'Toast Driven': 'http://toastdriven.com/feeds/fresh_news/',
    'Django': 'https://www.djangoproject.com/rss/weblog/',
}


class RSSFetcher(Fetcher):
    use = 'fetchers.stdlib.OldBroke'


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
        print '"%s" (%s): %s...' % (
            article['title'],
            urlparse.urlparse(article['link']).netloc,
            article.get('description', '')[:25]
        )


if __name__ == '__main__':
    main()
