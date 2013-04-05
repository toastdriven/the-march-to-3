from __future__ import unicode_literals
import codecs
import importlib
import os
from six import with_metaclass


class FetcherMetaclass(type):
    def __new__(cls, name, bases, attrs):
        use_path = attrs.pop(u'use', u'')
        new_klass = super(FetcherMetaclass, cls).__new__(cls, name, bases, attrs)

        if use_path:
            # Dynamically load the configured fetcher.
            # Because metaclasses.
            path_bits = use_path.split('.')
            module_path = '.'.join(path_bits[:-1])
            fetch_klass_name = path_bits[-1]
            fetch_module = importlib.import_module(module_path)
            fetch_klass = getattr(fetch_module, fetch_klass_name)
            new_klass._fetcher = fetch_klass()
        else:
            new_klass._fetcher = None

        return new_klass


class Fetcher(with_metaclass(FetcherMetaclass)):
    # The default.
    use = u'fetchers.stdlib.OldBroke'
    base_path = os.path.join(u'/tmp', u'feeds')

    def __init__(self):
        super(Fetcher, self).__init__()
        self._is_setup = False

    def setup(self):
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

        self._is_setup = True

    def fetch(self, title, url):
        if not self._is_setup:
            self.setup()

        base_filename = title.lower().replace(u' ', u'-') + u'.xml'
        file_path = os.path.join(self.base_path, base_filename)

        # Delegate off to the configured fetcher.
        content = self._fetcher.fetch(url)

        # Hooray context managers!
        with codecs.open(file_path, u'w', encoding=u'utf-8') as the_file:
            the_file.write(content)

        return file_path
