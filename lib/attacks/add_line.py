import typing

from lib.ehhh_attack import InjectionEhhhAttackTask


class AddLineEhhhAttackTask(InjectionEhhhAttackTask):
    @staticmethod
    def _prepare_headers(host: str) -> dict:
        return {' host': host}


def generate_task(urls: list, **kwargs) -> typing.Iterator[InjectionEhhhAttackTask]:
    yield from AddLineEhhhAttackTask.generate_task(urls)
