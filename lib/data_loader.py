from ipaddress import ip_network
from os.path import dirname, exists, join
import re
from typing import Union


class DataLoader:
    @classmethod
    def load_from_file(cls, filename) -> list:
        if not exists(filename):
            filename = join(dirname(__file__), filename)

        try:
            data = cls.parse(filename)
        except OSError as e:
            raise ValueError(f'Can\'t open/read file: {filename}. Error: {e}')

        return data

    @staticmethod
    def parse(filename: str) -> list:
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip()]


class BruteforceWordlistLoader(DataLoader):
    @classmethod
    def parse(cls, filename: str) -> list:
        data = []
        with open(filename, 'r') as f:
            for line in f:
                item = line.strip()
                if not item:
                    continue

                parsed_item = cls.parse_item(item)
                if type(parsed_item) is list:
                    data += parsed_item
                else:
                    data.append(parsed_item)

        return data

    @staticmethod
    def parse_item(item: str) -> Union[list, str]:
        if re.match(r'\d{2,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', item):
            return [format(ip) for ip in ip_network(item).hosts()]

        return item
