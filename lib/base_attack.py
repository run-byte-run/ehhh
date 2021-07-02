from abc import ABC, abstractmethod


class BaseAttack(ABC):
    def __init__(self, **kwargs):
        if 'wordlist' not in kwargs:
            raise ValueError(f'Invalid argument "wordlist" in __init__ "{self.__class__.__name__}" class.')

        self._wordlist = kwargs['wordlist']

    def generate_task(self, task_class, urls: list) -> list:
        tasks = []
        for word in self._wordlist:
            for url in urls:
                tasks.append(task_class(self, url, {'host': word}))
        return tasks

    @abstractmethod
    def execute(self, url: str, payload: dict) -> None:
        pass