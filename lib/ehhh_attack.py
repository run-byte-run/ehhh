from dataclasses import dataclass
from threading import Thread
from time import sleep
from queue import Queue

from lib.base_attack import BaseAttack


@dataclass
class EhhhAttackTask:
    module: BaseAttack
    url: str
    payload: dict

    def execute(self) -> None:
        class_name = self.module.__class__.__name__
        extends = f'Type: {class_name}, url: {self.url}, payload: {self.payload}.'

        if self.module.has_vulnerable(self.url, self.payload):
            print(f'Vulnerable found! {extends}')
        else:
            print(f'Just normal response :( {extends}')


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
                print(f'Exception {e}')
            finally:
                self._q.task_done()

    def run(self, urls: list, attacks: list) -> None:
        for attack in attacks:
            for task in attack.generate_task(EhhhAttackTask, urls):
                self._q.put(task)

        for _ in range(self.settings.get('thread', 10)):
            Thread(target=self.do_task, daemon=True).start()

        self._q.join()
