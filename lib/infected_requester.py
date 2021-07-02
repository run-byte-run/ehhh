from requests import session, Response
from typing import TypeVar

ListResponses = TypeVar('ListResponses', Response, Response)


class InfectedRequester:
    def __init__(self, headers: dict):
        headers.setdefault('user-agent', 'ehhh/0.1')
        self.headers = headers
        self.regular_cache = {}

    def get(self, url: str, inject_headers: dict) -> ListResponses:
        # make regular request to get cookies and data's.
        s = session()
        s.headers.update(self.headers)

        # cache regular request
        if url not in self.regular_cache:
            r = s.get(url)
            r.cookies.update(s.cookies)
            self.regular_cache[url] = r
        # set cookies
        for cookie in self.regular_cache[url].cookies:
            s.cookies.set(cookie.name, cookie.value)

        # make infected request
        s.headers.update(inject_headers)
        r = s.get(url)

        return [self.regular_cache[url], r]
