import re
import typing

from requests import Response

from lib.ehhh_attack import EhhhAttackTask


class BruteForceEhhhAttackTask(EhhhAttackTask):
    def _is_vulnerable(self, regular_response: Response, infected_response: Response) -> bool:
        if infected_response.status_code < 200 or infected_response.status_code > 303:
            return False

        return self._words_count(regular_response.text) != self._words_count(infected_response.text)

    @classmethod
    def _words_count(cls, text):
        stripped = cls._strip_tags(text)

        return len(stripped.split())

    @staticmethod
    def _strip_tags(text):
        return re.sub('<(script|style)[^<]+</(script|style)>', '', text)

    @staticmethod
    def _prepare_headers(host: str) -> dict:
        return {
            'host': host,
            ' host': host,
            'x-host': host,
            'x-forwarded-host': host,
            'x-forwarded-server': host,
            'x-real-host': host,
            'x-http-host-override': host,
            'forwarded': host,
        }


def generate_task(urls: list, **kwargs) -> typing.Iterator[BruteForceEhhhAttackTask]:
    for url in urls:
        for host in kwargs['wordlist']:
            yield BruteForceEhhhAttackTask(url, host)
