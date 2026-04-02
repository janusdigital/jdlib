class HttpError(Exception):
    def __init__(self, url, status):
        self.url = url
        self.status = status
        super().__init__(f'HTTP {status} for {url}')
