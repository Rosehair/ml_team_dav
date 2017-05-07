#!/home/vardges/anaconda3/bin/python
from argparse import ArgumentParser
import numpy as np
import sys


DESCRIPTION = 'csvcut - Select some columns from csv streem. Could change order of fields.'
EXAMPLES = 'example: csvcut -f 1,2 stat.txt'


def isEqual(a, b):
    return a == b


def isNotEqual(a, b):
    return a != b


def print_row(row, column_widths, output_stream):
    """
    Prints a row in human-readable format taking column widths into account

    :param row: row represented as a list of columns
    :param column_widths: a list of column list widths to be used for pretty printing
    :param output_stream: a stream to pretty print the row
    """
    output_line = '|'
    for i, column in enumerate(row):
        output_line += ' ' + column + ' ' * (column_widths[i] - len(column) + 1) + '|'
    output_line += '\n'
    output_stream.write(output_line)


def find_features(string_f, labels, unique=False, complement=False):
    """
    :param complement: if true, return indexes not in string_f
    :param unique: to take only unique fields
    :param string_f: feature string 
    :param labels: first row of the data
    :return: indexes of feature ti be shown
    """
    if complement:
        function_compare = isNotEqual
    else:
        function_compare = isEqual

    if len(string_f) is 0:
        features = []
    else:
        features = string_f.split(',')
        if unique:
            features = list(set(features))
    indexes = []
    for index, label in enumerate(labels):
        for feature in features:
            if function_compare(label, feature):
                indexes.append(index)
    print(indexes)
    return indexes


def filter_by_column(rows, indexes):
    """
    :param rows: original rows of file 
    :param indexes: indexes to only show in the end
    :return: new rows list
    """
    new_rows = []
    for row in rows:
        row_add = []
        for index in indexes:
            row_add.append(row[index])
        new_rows.append(row_add)

    return new_rows


def main():
    args = parse_args()
    input_stream = open(args.file, 'r') if args.file else sys.stdin
    num_lines = sum(1 for line in input_stream)
    input_stream = open(args.file, 'r') if args.file else sys.stdin
    output_stream = open(args.output_file, 'r') if args.output_file else sys.stdout

    first_rows = []
    for i in range(num_lines):
        first_rows.append(input_stream.readline().strip().split(args.separator))

    index_show = find_features(args.fields, first_rows[0], unique=args.unique, complement=args.complement)
    first_rows = filter_by_column(first_rows, index_show)
    columns = first_rows[0]
    column_widths = [max([len(column) for column in [row[i] for row in first_rows]]) for i in range(len(columns))]

    for row in first_rows:
        print_row(row, column_widths, output_stream)

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
    parser.add_argument('-c', '--complement', help='Instead of leaving only specified columns, leave all except specified', action='store_true')
    parser.add_argument('file', nargs='?', help='File to read input from. stdin is used by default')

    args = parser.parse_args()

    return args

main()
