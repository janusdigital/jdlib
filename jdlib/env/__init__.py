import os

_BOOL_TRUE = frozenset(('true', '1', 'yes'))
_BOOL_FALSE = frozenset(('false', '0', 'no', ''))


def _cast(value):
    if not isinstance(value, str):
        return value

    lower = value.lower()
    if lower in _BOOL_TRUE:
        return True
    if lower in _BOOL_FALSE:
        return False

    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    if ',' in value:
        return [_cast(item.strip()) for item in value.split(',') if item.strip()]

    return value


class Env:
    def __init__(self, **defaults):
        self.defaults = defaults

    def __call__(self, key, default=None, cast=None):
        value = os.environ.get(key, self.defaults.get(key, default))
        if value is None:
            return value
        if cast is not None:
            return cast(value)
        return _cast(value)

    def str(self, key, default=None):
        return self(key, default=default, cast=str)

    def bool(self, key, default=False):
        value = self(key, default=default)
        if isinstance(value, bool):
            return value
        if value is None:
            return default
        return str(value).lower() in _BOOL_TRUE

    def int(self, key, default=0):
        return self(key, default=default, cast=int)

    def float(self, key, default=0.0):
        return self(key, default=default, cast=float)

    def list(self, key, default=None, separator=','):
        value = self.str(key)
        if value is None:
            return default if default is not None else []
        if isinstance(value, list):
            return value
        return [item.strip() for item in value.split(separator) if item.strip()]
