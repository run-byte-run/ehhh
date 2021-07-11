import typing

from lib.ehhh_attack import InjectionEhhhAttackTask


class XHeaderAttackTask(InjectionEhhhAttackTask):
    @staticmethod
    def _prepare_headers(host: str) -> dict:
        return {
            'x-host': host,
            'x-forwarded-host': host,
            'x-forwarded-server': host,
            'x-real-host': host,
            'x-http-host-override': host,
            'forwarded': host,
        }


def generate_task(urls: list, **kwargs) -> typing.Iterator[XHeaderAttackTask]:
    yield from XHeaderAttackTask.generate_task(urls)
