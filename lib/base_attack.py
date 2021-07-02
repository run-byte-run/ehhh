from abc import ABC, abstractmethod
from requests import Response

import lib.ehhh_attack
from lib.infected_requester import InfectedRequester


class BaseAttack(ABC):
    def __init__(self, infected_requester: InfectedRequester, **kwargs):
        self.infected_requester = infected_requester

    def has_vulnerable(self, url: str, headers: dict) -> bool:
        [rr, ir] = self.infected_requester.get(url, headers)

        return self._is_vulnerable(rr, ir)

    @abstractmethod
    def generate_task(self, urls: list) -> list:
        pass

    @abstractmethod
    def _is_vulnerable(self, regular_response: Response, infected_response: Response) -> bool:
        return False


class WordlistAttack(BaseAttack, ABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # todo: change error type, to disable attack when that error raised.
        if 'wordlist' not in kwargs:
            raise ValueError(f'Invalid argument "wordlist" in __init__ "{self.__class__.__name__}" class.')

        self._wordlist = kwargs['wordlist']
        self._natural_responses = {}

    def generate_task(self, urls: list) -> list:
        tasks = []
        for host in self._wordlist:
            for url in urls:
                tasks.append(lib.ehhh_attack.EhhhAttackTask(self, url, self._get_inject_headers(host)))
        return tasks

    @staticmethod
    @abstractmethod
    def _get_inject_headers(host: str) -> dict:
        pass

    def _is_vulnerable(self, regular_response: Response, infected_response: Response) -> bool:
        if 400 <= infected_response.status_code < 500:
            return False

        return len(regular_response.text) != len(infected_response.text)
