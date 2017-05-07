from argparse import ArgumentParser
from collections import defaultdict
from signal import signal, SIGPIPE, SIG_DFL
import sys

DESCRIPTION = 'csvmap - Transform each row of a csv file with an expression provided.'
EXAMPLES = "example: cat file.csv | csvmap 'r[5] = float(r[12]) ** 2'"


def pr_string(str):
    """
    :param str: string to process 
    :return: string in which there is " after [ and before ]
    """
    new_str = str + ''
    index = 0
    while True:
        if new_str[index] is '[':
            new_str = new_str[0:index + 1] + '"' + new_str[index + 1:len(new_str)]
            index += 1
        if new_str[index] is ']':
            new_str = new_str[0:index] + '"' + new_str[index:len(new_str)]
            index += 1
        index += 1
        if index >= len(new_str):
            break
    return new_str


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


def map_line(row, labels, expression, EXEC):
    """
    chnage each row of the file
    :param row: row to change 
    :param labels: list of labels
    :param expression: expression for map operation
    :param EXEC: exec it before changing the row
    :return: 
    """
    r = defaultdict(None, zip(labels, row))
    exec(EXEC)
    exec(expression)
    new_row = []
    keys = []
    for key, value in r.items():
        new_row.append(str(value))
        keys.append(str(key))
    return new_row, keys


def main():
    signal(SIGPIPE, SIG_DFL)
    args = parse_args()
    expression = pr_string(args.expression)

    input_stream = open(args.file, 'r') if args.file else sys.stdin
    output_stream = open(args.output_file, 'r') if args.output_file else sys.stdout

    first_row = input_stream.readline().strip().split(args.separator)
    key_printed = False
    while True:
        row = input_stream.readline()
        if len(row) is 0:
            break
        row = row.strip().split(args.separator)
        new_row, keys = map_line(row, first_row, expression, args.EXEC)
        if not key_printed:
            print_row(keys, output_stream)
            key_printed = True
        print_row(new_row, output_stream)

    if input_stream != sys.stdin:
        input_stream.close()
    if output_stream != sys.stdout:
        output_stream.close()


def parse_args():
    parser = ArgumentParser(description=DESCRIPTION, epilog=EXAMPLES)
    parser.add_argument('-s', '--separator', type=str, help='Separator to be used', default=',')
    parser.add_argument('-o', '--output_file', type=str, help='Output file. stdout is used by default')
    parser.add_argument('-e', '--EXEC', type=str, help='Execute python code before starting the transformation. '
                                                       'Might be useful for import statements or even for python '
                                                       'functions definition')
    parser.add_argument('file', nargs='?', help='File to read input from. stdin is used by default')
    parser.add_argument('expression', nargs='?', type=str, default='',
                        help="Python expression to be used to transform a row. Specific "
                             "columns can be referred as a fields of row object named r")

    args = parser.parse_args()
    return args


main()
