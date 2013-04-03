import importlib
import os


class FetcherMetaclass(type):
    def __new__(cls, name, bases, attrs):
        use_path = attrs.pop('use', '')
        new_klass = super(FetcherMetaclass, cls).__new__(cls, name, bases, attrs)

        # Dynamically load the configured fetcher.
        # Because metaclasses.
        path_bits = use_path.split('.')
        module_path = '.'.join(path_bits[:-1])
        fetch_klass_name = path_bits[-1]
        fetch_module = importlib.import_module(module_path)
        fetch_klass = getattr(fetch_module, fetch_klass_name)

        new_klass._fetcher = fetch_klass()
        return new_klass


class Fetcher(object):
    __metaclass__ = FetcherMetaclass
    # The default.
    use = 'fetchers.stdlib.OldBroke'
    base_path = os.path.join('/tmp', 'feeds')

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

        base_filename = title.lower().replace(' ', '-') + '.xml'
        file_path = os.path.join(self.base_path, base_filename)

        # Delegate off to the configured fetcher.
        content = self._fetcher.fetch(url)

        the_file = open(file_path, 'w')
        the_file.write(content)
        # BAD PROGRAMMER, NO CLOSE, NO COOKIE

        return file_path
