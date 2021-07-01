import argparse

from lib.data_loader import DataLoader
from lib.ehhh_attack import EhhhAttack

if __name__ == 'main':
    parser = argparse.ArgumentParser(description='Exploit HTTP Host Header.')
    parser.add_argument('--thread', type=int, default=10,
                        help='Thread count.')
    parser.add_argument('--wait', type=float, default=0.1,
                        help='Seconds timeout before each task.')
    parser.add_argument('-o', '--output', type=str,
                        help='Output into file instead of console.')
    parser.add_argument('-w', '--wordlist', type=str, default='payload/default.txt',
                        help='The path to file containing hostnames that will be used to attack payload.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--url', type=str, nargs='*',
                       help='Destination urls.')
    group.add_argument('--URL', type=str,
                       help='Destination urls from file.')
    attack_list = []
    parser.add_argument('--attack', type=str, nargs='+', default='all', choices=attack_list,
                        help='The attack names.')

    args = parser.parse_args()

    urls = [args.url] if args.url else DataLoader.load_from_file(args.URL)

    ehhAttack = EhhhAttack(thread=args.thread, wait=args.wait, output=args.output)
    ehhAttack.run(urls, args.attack)
