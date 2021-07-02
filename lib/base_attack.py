from abc import ABC, abstractmethod
import requests


class BaseAttack(ABC):
    def __init__(self, headers, **kwargs):
        self._headers = {**{'user-agent': 'ehhh/0.1'}, **headers}

    @abstractmethod
    def generate_task(self, task_class, urls: list) -> list:
        pass

    @abstractmethod
    def has_vulnerable(self, url: str, payload: dict) -> bool:
        pass

    @abstractmethod
    def _is_vulnerable_response(self, url: str, status_code: int, response: str) -> bool:
        pass


class WordlistAttack(BaseAttack, ABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'wordlist' not in kwargs:
            raise ValueError(f'Invalid argument "wordlist" in __init__ "{self.__class__.__name__}" class.')

        self._wordlist = kwargs['wordlist']
        self._natural_responses = {}

    def generate_task(self, task_class, urls: list) -> list:
        tasks = []
        for word in self._wordlist:
            for url in urls:
                tasks.append(task_class(self, url, {'host': word}))
        return tasks

    def has_vulnerable(self, url: str, payload: dict) -> bool:
        r = requests.get(url, headers={
            **self._headers,
            **self._inject_header(payload['host'])
        })
        return self._is_vulnerable_response(url, r.status_code, r.text)

    @abstractmethod
    def _inject_header(self, host: str) -> dict:
        pass

    def _is_vulnerable_response(self, url: str, status_code: int, response: str) -> bool:
        if 400 <= status_code < 500:
            return False

        return len(response) != len(self._do_natural_request(url))

    def _do_natural_request(self, url: str) -> str:
        if url not in self._natural_responses:
            r = requests.get(url, headers=self._headers)
            self._natural_responses[url] = r.text
        return self._natural_responses[url]
