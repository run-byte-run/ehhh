from lib.base_attack import WordlistAttack


class FlawedAttack(WordlistAttack):
    def execute(self, url: str, payload: dict) -> None:
        pass