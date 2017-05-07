from argparse import ArgumentParser
import sys


DESCRIPTION = 'csvpp - prints cvs file in human-readable format'
EXAMPLES = 'example: cat file.txt | csvpp -n 20 | less -SR'


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


def print_separetor(column_widths, output_stream):
    """
    Prints separetor line with ----
    :param column_widths: a list of column list widths to be used for pretty printing
    :param output_stream: a stream to pretty print the row
    """
    output_line = '-'
    for width in column_widths:
        output_line += '-' * (width+3)
    output_line += '\n'
    output_stream.write(output_line)


def main():
    args = parse_args()
    input_stream = open(args.file, 'r') if args.file else sys.stdin
    output_stream = open(args.output_file, 'w') if args.output_file else sys.stdout

    columns = input_stream.readline().strip().split(args.separator)
    first_rows = [columns]
    for i in range(args.column):
        stream = input_stream.readline().strip().split(args.separator)
        if len(stream) < len(columns):
            break
        first_rows.append(stream)

    column_widths = [max([len(column) for column in [row[i] for row in first_rows]]) for i in range(len(columns))]

    num_lines = args.lines_number + 1
    for index, row in enumerate(first_rows):
        if num_lines == 0:
            break
        num_lines -= 1
        if index is 1:
            print_separetor(column_widths, output_stream)
        print_row(row, column_widths, output_stream)

    while True:
        row = input_stream.readline()
        if num_lines == 0 or len(row) is 0:
            break
        num_lines -= 1
        print_row(row.strip().split(args.separator), column_widths, output_stream)

    if input_stream != sys.stdin:
        input_stream.close()
    if output_stream != sys.stdout:
        output_stream.close()


def parse_args():
    parser = ArgumentParser(description=DESCRIPTION, epilog=EXAMPLES)
    parser.add_argument('-s', '--separator', type=str, help='Separator to be used', default=',')
    parser.add_argument('-c', '--column', type=int, help='Number of lines used to set column width', default=30)
    parser.add_argument('-n', '--lines_number', type=int, help='Number of lines to show', default=100)
    parser.add_argument('-o', '--output_file', type=str, help='Output file. stdout is used by default')

    parser.add_argument('file', nargs='?', help='File to read input from. stdin is used by default')

    args = parser.parse_args()

    return args

main()
