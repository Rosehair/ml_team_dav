#!/home/david/miniconda3/bin/python3
import sys
from argparse import ArgumentParser

DESCRIPTION = 'csvhead - pipes the first lines from csv file'
EXAMPLE = 'csvhead -n 50 example.txt'


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('-n', '--number_of_lines', type=int, help='number of lines to pass', default=10)
    parser.add_argument('-o', '--output_file', type=str, help='output file. stdout is used by default')

    parser.add_argument('file', nargs='?', help='File to read input from. stdin is used by default')
    return parser.parse_args()


def main():
    args = parse_arguments()
    input_stream = open(args.file, 'r') if args.file else sys.stdin
    output_stream = open(args.output_file, 'w') if args.output_file else sys.stdout

    lines = 0
    while True:
        lines += 1
        row = input_stream.readline()
        if lines <= args.number_of_lines and len(row) is not 0:
            output_stream.write(row)
        else:
            break

    if input_stream != sys.stdin:
        input_stream.close()
    if output_stream != sys.stdout:
        output_stream.close()


main()
