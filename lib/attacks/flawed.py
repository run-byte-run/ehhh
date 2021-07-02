from lib.base_attack import WordlistAttack

SUFFIX_LIST = [':ehhh-port', '/ehhh-stuff']


class FlawedAttack(WordlistAttack):
    def _inject_header(self, host: str) -> dict:
        return {'host': host}

    def generate_task(self, task_class, urls: list) -> list:
        tasks = []
        for word in self._wordlist:
            for url in urls:
                for suffix in SUFFIX_LIST:
                    tasks.append(task_class(self, url, {'host': word + suffix}))
        return tasks
