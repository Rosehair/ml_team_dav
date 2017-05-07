#!/home/david/miniconda3/bin/python3
from argparse import ArgumentParser
from signal import signal, SIGPIPE, SIG_DFL
import numpy as np
import sys
from utils import *

DESCRIPTION = 'csvcut - Select some columns from csv streem. Could change order of fields.'
EXAMPLES = 'example: csvcut -f 1,2 stat.txt'


def print_row(row, output_stream):
    """
    Prints a row in csv format
    :param row: row represented as a list of columns
    :param output_stream: a stream to pretty print the row
    """
    output_line = ''
    for index, column in enumerate(row):
        if index is 0:
            output_line += column
        else:
            output_line += ',' + column
    output_line += '\n'
    output_stream.write(output_line)


def main():
    signal(SIGPIPE, SIG_DFL)
    args = parse_args()

    input_stream = open(args.file, 'r') if args.file else sys.stdin
    output_stream = open(args.output_file, 'r') if args.output_file else sys.stdout

    first_row = input_stream.readline().strip().split(args.separator)
    index_show = find_features(args.fields, first_row, unique=args.unique)
    print_row(filter_by_column(first_row, index_show), output_stream)

    while True:
        row = input_stream.readline()
        if len(row) is 0:
            break
        row = row.strip().split(args.separator)
        row = filter_by_column(row, index_show)
        print_row(row, output_stream)

    if input_stream != sys.stdin:
        input_stream.close()
    if output_stream != sys.stdout:
        output_stream.close()


def parse_args():
    parser = ArgumentParser(description=DESCRIPTION, epilog=EXAMPLES)
    parser.add_argument('-s', '--separator', type=str, help='Separator to be used', default=',')
    parser.add_argument('-f', '--fields', type=str, help='Specify list of fields (comma separated) to cut', default='')
    parser.add_argument('-o', '--output_file', type=str, help='Output file. stdout is used by default')
    parser.add_argument('-u', '--unique', help='Remove duplicates from list of FIELDS', action='store_true')
    parser.add_argument('file', nargs='?', help='File to read input from. stdin is used by default')

    args = parser.parse_args()

    return args

main()
