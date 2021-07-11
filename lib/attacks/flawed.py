import typing

from lib.ehhh_attack import InjectionEhhhAttackTask


class FlawedEhhhAttackTask(InjectionEhhhAttackTask):
    pass


def generate_task(urls: list, **kwargs) -> typing.Iterator[FlawedEhhhAttackTask]:
    yield from FlawedEhhhAttackTask.generate_task(urls)
