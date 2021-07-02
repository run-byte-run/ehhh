from lib.base_attack import WordlistAttack


class AddLineAttack(WordlistAttack):
    @staticmethod
    def _get_inject_headers(url: str, host: str) -> dict:
        return {' host': host}
