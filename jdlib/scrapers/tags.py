from bs4 import BeautifulSoup


def soupify(html):
    return BeautifulSoup(html, 'html.parser')


class NullableTag:
    def __init__(self, tag=None):
        self._tag = tag

    def find(self, *args, **kwargs):
        if self._tag is None:
            return NullableTag()
        return NullableTag(self._tag.find(*args, **kwargs))

    def find_all(self, *args, **kwargs):
        if self._tag is None:
            return []
        return self._tag.find_all(*args, **kwargs)

    def get_text(self, *args, **kwargs):
        if self._tag is None:
            return ''
        return self._tag.get_text(*args, **kwargs)

    def decode_contents(self, *args, **kwargs):
        if self._tag is None:
            return ''
        return self._tag.decode_contents(*args, **kwargs)

    @property
    def string(self):
        if self._tag is None:
            return None
        return self._tag.string

    @property
    def text(self):
        if self._tag is None:
            return ''
        return self._tag.get_text(strip=True)

    def get(self, key, default=None):
        if self._tag is None:
            return default
        return self._tag.get(key, default)

    def __getitem__(self, key):
        if self._tag is None:
            raise KeyError(key)
        return self._tag[key]

    def __bool__(self):
        return self._tag is not None

    def __repr__(self):
        if self._tag is None:
            return None
        return f'NullableTag({self._tag!r})'
