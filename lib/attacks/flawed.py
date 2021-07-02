from lib.base_attack import WordlistAttack
import lib.ehhh_attack

SUFFIX_LIST = ['', ':ehhh-port', '/ehhh-stuff']


class FlawedAttack(WordlistAttack):
    def _get_inject_headers(self, host: str) -> dict:
        return {'host': host}

    def generate_task(self, urls: list) -> list:
        tasks = []
        for host in self._wordlist:
            for url in urls:
                for suffix in SUFFIX_LIST:
                    tasks.append(
                        lib.ehhh_attack.EhhhAttackTask(self, url, self._get_inject_headers(host + suffix))
                    )
        return tasks
