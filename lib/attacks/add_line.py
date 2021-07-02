from http import client
from lib.base_attack import WordlistAttack
import re

client._is_legal_header_name = re.compile(rb'[^:][^:\r\n]*').fullmatch


class AddLineAttack(WordlistAttack):
    @staticmethod
    def _get_inject_headers(host: str) -> dict:
        return {' host': host}
