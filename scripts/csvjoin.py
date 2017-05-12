from argparse import ArgumentParser
import operator
import sys
import csv

DESCRIPTION = 'csvtail - Join two csv files using the keys provided.'
EXAMPLES = 'examples: csvjoin stat1.txt stat2.txt -k id, -t OUTER'
'''
csvjoin

usage: csvjoin [-h] [-q] [--careful] [-s SEPARATOR] [-o OUTPUT_FILE] [-k KEYS] [-c CONFLICT_PREFIX] [-t TYPE] file2 [file]

Join two csv files using the keys provided.

positional arguments: file

File to read input from. stdin is used by default
file2

File to join with
optional arguments: -h, --help

show help message and exit
-q, --quiet

Don't print information regarding errors
--careful

Stop if input contains an incorrect row
-s SEPARATOR, --separator SEPARATOR

Separator to be used
-k KEYS, --fields KEYS

Comma-separated list of columns to be used as reduce keys. Column names or column numbers can be used here. These columns will be used as the join keys.
-c CONFLICT_PREFIX, --conflict_prefix CONFLICT_PREFIX

Specify a prefix to be used for the columns taken from file2 having the same names. Default is conflict_
-t TYPE, --type TYPE

Type of join to be used. Either INNER, LEFT or OUTER. INNER is default.
-o OUTPUT_FILE, --output_file OUTPUT_FILE

Output file. stdout is used by default
examples: csvjoin stat1.txt stat2.txt -k id, -t OUTER
'''

BLOCK_SIZE = 1024



def main():
    args = parse_args()
    input_file = open(args.file)
    input_file2 = open(args.file2) if args.file2 else sys.stdin
    output_stream = open(args.output_file, 'w') if args.output_file else sys.stdout

    keys = args.keys.strip().split(args.separator)

    headline_str = input_file.readline()
    headline = headline_str.strip().split(args.separator)
    headline = {k: i for i, k in enumerate(headline)}
    if all(map(lambda x: x.isdigit() or x == '-', keys)):
        keys = [int(key) for key in keys]
        pass
    else:
        keys = [headline[key] for key in keys]


    headline_str2 = input_file2.readline()
    headline2 = headline_str2.strip().split(args.separator)
    headline2 = {k: i for i, k in enumerate(headline2)}
    assert(all([True if headline2.get(key,None) is None else False for key in keys]))
    L = []

    writer = csv.writer(output_stream, delimiter=args.separator, lineterminator='\n')
    writer.writerow(headline.keys())

    for line in input_file:
        line = line.strip().split(args.separator)
        line = [line[key] for key in keys]
        L.append(line)
        writer.writerow(line)

    for line in input_file2:
        line = line.strip().split(args.separator)
        line = [line[key] for key in keys]
        for line_to_compare in L:
            for i in range(len(keys)):
                if line[i] == line_to_compare[i]:
                    line[i] = args.conflict_prefix + line[i]
        writer.writerow(line)




def parse_args():
    parser = ArgumentParser(description=DESCRIPTION, epilog=EXAMPLES)
    parser.add_argument('-n', '--number_of_lines', type=int, help='Number of last rows to print if positive '
                                                                  'NUMBER_OF_LINES. Else skips NUMBER_OF_LINES lines '
                                                                  'and prints till the end of input. Default 10.',
                        default=10)
    parser.add_argument('-o', '--output_file', type=str, help='Output file. stdout is used by default')
    parser.add_argument('-q', '--quiet',action='store_true', help='Don\'t print information regarding errors')
    parser.add_argument('-s', '--separator', type=str, help='Separator to be used', default=',')
    parser.add_argument('-k', '--keys', type=str, help='Comma-separated list of columns to be used as reduce keys. Column names or column numbers can be used here. These columns will be used as the join keys.')
    parser.add_argument('-c', '--conflict_prefix', type=str, help='Specify a prefix to be used for the columns taken from file2 having the same names. Default is \'conflict_\'.', default='conflict_')
    parser.add_argument('-t', '--type', type=str, help='Type of join to be used. Either INNER, LEFT or OUTER. INNER is default.')
    parser.add_argument('file', nargs='?', help='File to read input from. stdin is used by default')
    parser.add_argument('file2', nargs='?', help='File to join with')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    main()