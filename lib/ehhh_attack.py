from __future__ import annotations
from abc import ABC, abstractmethod
from http import client
import logging
import re
from threading import Thread
from time import sleep
import typing
from queue import Queue

from requests import Response
from requests.exceptions import RequestException
from termcolor import cprint

from lib.infected_requester import InfectedRequester
from lib.utils import get_domain_from_url

# monkey patch to allow space in header
client._is_legal_header_name = re.compile(rb'[^:][^:\r\n]*').fullmatch


class EhhhAttackTask(ABC):
    def __init__(self, url: str, host: str):
        self.url = url
        self.host = host
        self.headers = self._prepare_headers(host)

    @property
    def name(self):
        return self.__class__.__name__

    def execute(self, infected_requester: InfectedRequester) -> bool:
        [rr, ir] = infected_requester.get(self.url, self.headers)

        return self._is_vulnerable(rr, ir)

    @staticmethod
    def _prepare_headers(host: str) -> dict:
        return {'host': host}

    @abstractmethod
    def _is_vulnerable(self, regular_response: Response, infected_response: Response) -> bool:
        pass


class InjectionEhhhAttackTask(EhhhAttackTask):
    SUFFIX_LIST = [':ehhh-port', '/ehhh-stuff']

    @property
    def match_pattern(self) -> re.Pattern:
        return re.compile(self.host)

    def _is_vulnerable(self, regular_response: Response, infected_response: Response) -> bool:
        return self.match_pattern.search(infected_response.text) is not None

    @classmethod
    def generate_task(cls, urls: list) -> typing.Iterator[InjectionEhhhAttackTask]:
        for url in urls:
            for suffix in cls.SUFFIX_LIST:
                yield cls(url, get_domain_from_url(url) + suffix)


class EhhhAttack:
    def __init__(self, infected_requester: InfectedRequester, **settings: dict) -> None:
        self.infected_requester = infected_requester
        self.settings = {**{'thread': 10, 'wait': 0.1}, **settings}
        self._q = Queue(self.settings['thread'] * 2)

    def do_task(self):
        while True:
            sleep(self.settings['wait'])

            task = self._q.get()
            try:
                if task.execute(self.infected_requester):
                    cprint(f'Task "{task.name}" with "host: {task.host}" may be vulnerability!', 'green')
            except RequestException as e:
                logging.warning(e)
            finally:
                self._q.task_done()

    def run(self, urls: list, modules: list, **kwargs) -> None:
        cprint(f'Ehhh just run...', 'cyan')

        for _ in range(self.settings['thread']):
            Thread(target=self.do_task, daemon=True).start()

        try:
            for module in modules:
                cprint(f'Module "{module.__name__} generate task.', 'cyan')
                for task in module.generate_task(urls, **kwargs):
                    self._q.put(task)

            self._q.join()
        except KeyboardInterrupt:
            cprint('Terminate...', 'cyan')
