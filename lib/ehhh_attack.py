from dataclasses import dataclass
import logging
from threading import Thread
from time import sleep
from queue import Queue

from termcolor import cprint

import lib.base_attack


@dataclass
class EhhhAttackTask:
    module: lib.base_attack.BaseAttack
    url: str
    headers: dict

    def execute(self) -> None:
        if self.module.has_vulnerable(self.url, self.headers):
            class_name = self.module.__class__.__name__
            extends = f'Type: {class_name}, url: {self.url}, headers: {self.headers}.'
            cprint(f'Hmm, non-standard behaviour! {self.module.get_vulnerable_text()} {extends}', 'green')


class EhhhAttack:
    def __init__(self, **settings: dict) -> None:
        self.settings = settings
        self._q = Queue()

    def do_task(self):
        while True:
            sleep(self.settings.get('wait', 0.1))

            task = self._q.get()
            try:
                task.execute()
            except Exception as e:
                logging.warning(e)
            finally:
                self._q.task_done()

    def run(self, urls: list, attacks: list) -> None:
        for attack in attacks:
            for task in attack.generate_task(urls):
                self._q.put(task)

        for _ in range(self.settings.get('thread', 10)):
            Thread(target=self.do_task, daemon=True).start()

        self._q.join()
