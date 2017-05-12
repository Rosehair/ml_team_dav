from argparse import ArgumentParser
import operator
import csv

import sys


DESCRIPTION = 'csvtail - Sort the rows of csv stream ascending.'
EXAMPLES = 'examples: cat stat.csv | csvsort -k shows'


BLOCK_SIZE = 1024

'''
csvsort

usage: csvsort [-h] [-s SEPARATOR] [-o OUTPUT_FILE] [-k KEYS] [-m MAX_ROWS] [--descending] [--numeric] [file]

Sort the rows of csv stream ascending.

positional arguments: file

File to read input from. stdin is used by default
optional arguments: -h, --help

show help message and exit
-s SEPARATOR, --separator SEPARATOR

Separator to be used
-k KEYS, --keys KEYS

Specify the list of keys (comma separated) to sort on. Field names or field numbers can be used. Dash can be used to specify fields ranges. Range 'F1-F2' stands for all fields between F1 and F2. Range '-F2' stands for all fields up to F2. Range 'F1-' stands for all fields from F1 til the end.
--descending

If provided, perform descending sort instead of ascending
--numeric

If provided, keys will be interpreted as numbers. Otherwise - as strings.
-m MAX_ROWS, --max-rows MAX_ROWS

Don't load to memory more than MAX_ROWS rows at a time. This option is crucial if you have to deal with huge csv files. Default value is 0 that meanse that this will sort file in memory.
-o OUTPUT_FILE, --output_file OUTPUT_FILE

Output file. stdout is used by default
examples: cat stat.csv | csvsort -k shows
'''
import pandas as pd


def main():
    args = parse_args()
    input_stream = open(args.file, 'r') if args.file else sys.stdin
    output_stream = open(args.output_file, 'w') if args.output_file else sys.stdout
    args.keys = args.keys.replace('-', args.separator + '-' + args.separator)
    keys = args.keys.strip().split(args.separator)

    headline_str = input_stream.readline()
    headline = headline_str.strip().split(args.separator)
    headline = {k: i for i, k in enumerate(headline)}
    if all(map(lambda x: x.isdigit() or x == '-', keys)):
        keys = [int(key) for key in keys]
        pass
    else:
        keys = [headline[key] for key in keys]
    L = []
    for line in input_stream:
        line = line.strip().split(args.separator)
        if args.numeric:
            for key in keys:
                line[key] = int(line[key])
        L.append(line)

    print(operator.itemgetter(*keys)(L[1]))

    L.sort(key=operator.itemgetter(*keys), reverse=args.descending)
    writer = csv.writer(output_stream, delimiter=args.separator, lineterminator='\n')
    writer.writerow(headline.keys())
    for line in L:
        writer.writerow(line)



def parse_args():
    parser = ArgumentParser(description=DESCRIPTION, epilog=EXAMPLES)
    parser.add_argument('-s', '--separator', type=str, help='Separator to be used', default=',')

    parser.add_argument('-k', '--keys', type=str, help='Specify the list of keys (comma separated) to sort on. Field names or field numbers can be used. Dash can be used to specify fields ranges. Range \'F1-F2\' stands for all fields between F1 and F2. Range \'-F2\' stands for all fields up to F2. Range \'F1-\' stands for all fields from F1 til the end.', default='')
    parser.add_argument('-m', '--max-rows', type=int, help='Don\'t load to memory more than MAX_ROWS rows at a time. This option is crucial if you have to deal with huge csv files. Default value is 0 that meanse that this will sort file in memory.')

    parser.add_argument('--descending', action='store_true', help='If provided, perform descending sort instead of ascending')
    parser.add_argument('--numeric', action='store_true', help='If provided, keys will be interpreted as numbers. Otherwise - as strings.')

    parser.add_argument('-o', '--output_file', type=str, help='Output file. stdout is used by default')
    parser.add_argument('file', nargs='?', help='File to read input from. stdin is used by default')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    main()