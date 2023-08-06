"""Command Line Interface"""

import argparse
import os
from .sorting import sort_by_counting

parser = argparse.ArgumentParser(description='Sorting an array')
parser.add_argument('-s', '--sort', action='store_true',
    help='sort an array by counting',)
parser.add_argument('-t', '--test', action='store_true',
    help='start tests and show report')
parser.add_argument('-a', '--array', type=int, nargs='+', metavar='',
    default=0, help='list of integers to be sorted')

args = parser.parse_args()

if __name__ == '__main__':
    if args.sort:
        print(sort_by_counting(args.array))
    if args.test:
        os.system('cd sorting_array & python -m pytest tests -v')
