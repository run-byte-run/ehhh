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
        self.settings = {**{
            'thread': 10,
            'wait': 0.1,
        }, **settings}
        self._q = Queue(self.settings['thread'] * 2)

    def do_task(self):
        while True:
            sleep(self.settings['wait'])

            task = self._q.get()
            try:
                self._print_remaining_task()
                task.execute()
            except Exception as e:
                logging.warning(e)
            finally:
                self._q.task_done()

    # @todo: do it better
    def _print_remaining_task(self):
        qsize = self._q.qsize()
        if qsize % 100 == 0:
            cprint(f'Remaining tasks: {qsize}', 'cyan')

    def run(self, urls: list, attacks: list) -> None:
        cprint(f'Ehhh just run...', 'cyan')

        for _ in range(self.settings['thread']):
            Thread(target=self.do_task, daemon=True).start()

        try:
            for attack in attacks:
                cprint(f'Attack: {attack.name}', 'cyan')
                for task in attack.generate_task(urls):
                    self._q.put(task)

            self._q.join()
        except KeyboardInterrupt:
            cprint('Terminate...', 'cyan')
