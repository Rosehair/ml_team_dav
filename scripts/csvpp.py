from argparse import ArgumentParser
import sys
import numbers
from signal import signal, SIGPIPE, SIG_DFL

signal(SIGPIPE, SIG_DFL)

DESCRIPTION = 'csvpp - prints cvs file in human-readable format'
EXAMPLES = 'example: cat file.txt | csvpp -n 20 | less -SR'


def format_string_float(value, do_it=False):
    """
    :param do_it: do format strings
    :param value: string in our csv 
    :return: float number if possible to format
    """
    if do_it:
        try:
            element = float(value)
            if len(value) > 5:
                return str("{0:.3e}".format(float(element)))
            else:
                return value
        except ValueError:
            return value
    else:
        return value


def print_row(row, column_widths, output_stream, print_nice):
    """
    Prints a row in human-readable format taking column widths into account

    :param print_nice: bool that indicates to print float nicely
    :param row: row represented as a list of columns
    :param column_widths: a list of column list widths to be used for pretty printing
    :param output_stream: a stream to pretty print the row
    """
    output_line = '|'
    for i, column in enumerate(row):
        if print_nice:
            column = format_string_float(column, print_nice)
        output_line += ' ' + column + ' ' * (column_widths[i] - len(column) + 1) + '|'
    output_line += '\n'
    output_stream.write(output_line)


def print_separator(column_widths, output_stream):
    """
    Prints separator line with ----
    :param column_widths: a list of column list widths to be used for pretty printing
    :param output_stream: a stream to pretty print the row
    """
    output_line = '-'
    for width in column_widths:
        output_line += '-' * (width + 3)
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

    column_widths = [
        max([len(format_string_float(column, args.format_floats)) for column in [row[i] for row in first_rows]])
        for i in range(len(columns))]

    num_lines = args.lines_number + 1
    for index, row in enumerate(first_rows):
        if num_lines == 0:
            break
        num_lines -= 1
        if index is 1:
            print_separator(column_widths, output_stream)
        print_row(row, column_widths, output_stream, args.format_floats)

    for row in input_stream:
        if num_lines == 0:
            break
        num_lines -= 1
        print_row(row.strip().split(args.separator), column_widths, output_stream, args.format_floats)

    if input_stream != sys.stdin:
        input_stream.close()
    if output_stream != sys.stdout:
        output_stream.close()


def parse_args():
    parser = ArgumentParser(description=DESCRIPTION, epilog=EXAMPLES)
    parser.add_argument('-s', '--separator', type=str, help='Separator to be used', default=',')
    parser.add_argument('-c', '--column', type=int, help='Number of lines used to set column width', default=30)
    parser.add_argument('-n', '--lines_number', type=int, help='Number of lines to show', default=100)
    parser.add_argument('-f', '--format_floats', help='formats float nicely', action='store_true')
    parser.add_argument('-o', '--output_file', type=str, help='Output file. stdout is used by default')
    parser.add_argument('file', nargs='?', help='File to read input from. stdin is used by default')

    args = parser.parse_args()

    return args


main()
