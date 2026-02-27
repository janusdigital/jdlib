import os


class Env:
    def __init__(self, **defaults):
        self.defaults = defaults

    def str(self, key, default=None):
        value = self.defaults.get(key, default)
        return os.environ.get(key, value)

    def bool(self, key, default=False):
        value = self.str(key)
        if value is None:
            return default
        if isinstance(value, bool):
            return value
        return value.lower() in ('true', '1', 'yes')

    def list(self, key, default=None, separator=','):
        value = self.str(key)
        if value is None:
            return default if default is not None else []
        if isinstance(value, list):
            return value
        return [item.strip() for item in value.split(separator) if item.strip()]
