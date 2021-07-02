from lib.base_attack import WordlistAttack


class AddLineAttack(WordlistAttack):
    def _inject_header(self, host: str) -> dict:
        return {' host': host}
