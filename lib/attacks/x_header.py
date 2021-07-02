from lib.base_attack import WordlistAttack


class XHeaderAttack(WordlistAttack):
    def _get_inject_headers(self, host: str) -> dict:
        return {
            'x-host': host,
            'x-forwarded-host': host,
            'x-forwarded-server': host,
            'x-real-host': host,
            'x-http-host-override': host,
            'forwarded': host,
        }
