from argparse import ArgumentParser
from collections import defaultdict
from utils import report_error, report_wrong_number_of_columns, InputError, report_wrong_expression, report_wrong_exec
import sys

DESCRIPTION = 'csvmap - Transform each row of a csv file with an expression provided.'
EXAMPLES = "example: cat file.csv | csvmap 'r[5] = float(r[12]) ** 2'"


def format_string(my_str):
    """
    formats string to expression to be more easy to type
    for example r[a] = r[b] instead of r["a"] = r["b"]
    :param my_str: string to process 
    :return: string in which there is " after [ and before ]
    """
    new_str = my_str + ''
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
    output_line = ','.join(row)
    output_line += '\n'
    output_stream.write(output_line)


def map_line(row, labels, expression, EXEC, args):
    """
    chnage each row of the file
    :param row: row to change 
    :param labels: list of labels
    :param expression: expression for map operation
    :param EXEC: exec it before changing the row
    :return: 
    """
    r = defaultdict(None, zip(labels, row))
    try:
        exec(EXEC)
    except:
        report_wrong_exec(EXEC, args.careful, args.quiet)
        return False, False
    try:
        exec(expression)
    except:
        report_wrong_expression(expression, args.careful, args.quiet)
        return False, False

    new_row = []
    keys = []
    for key, value in r.items():
        new_row.append(str(value))
        keys.append(str(key))
    return new_row, keys


def main():
    args = parse_args()
    input_stream = sys.stdin
    output_stream = sys.stdout
    try:
        if args.file:
            input_stream = open(args.file, 'r')
        if args.output_file:
            output_stream = open(args.output_file, 'w')

        expression = format_string(args.expression)
        first_row = input_stream.readline().strip().split(args.separator)

        key_printed = False
        for row in input_stream:
            row = row.strip().split(args.separator)

            if len(row) != len(first_row):
                report_wrong_number_of_columns(row, args.careful, args.quiet)
                continue
            new_row, keys = map_line(row, first_row, expression, args.EXEC, args)
            if new_row is False:
                break
            if not key_printed:
                print_row(keys, output_stream)
                key_printed = True
            print_row(new_row, output_stream)

    except FileNotFoundError:
        report_error("File {} doesn't exist".format(args.file))
    except InputError as e:
        report_error(e.message + '. Row: ' + str(e.expression))
    except KeyboardInterrupt:
        pass
    except BrokenPipeError:
        sys.stderr.close()
    except Exception as e:
        report_error('Caught unknown exception. Please report to developers: {}'.format(e))
    finally:
        if input_stream and input_stream != sys.stdin:
            input_stream.close()
        if output_stream:
            output_stream.close()


def parse_args():
    parser = ArgumentParser(description=DESCRIPTION, epilog=EXAMPLES)
    parser.add_argument('-s', '--separator', type=str, help='Separator to be used', default=',')
    parser.add_argument('-o', '--output_file', type=str, help='Output file. stdout is used by default')
    parser.add_argument('-e', '--EXEC', type=str, help='Execute python code before starting the transformation. '
                                                       'Might be useful for import statements or even for python '
                                                       'functions definition', default='')
    parser.add_argument('-q', '--quiet', help="Don't print information regarding errors", action='store_true')
    parser.add_argument('--careful', help='Stop if input contains an incorrect row', action='store_true')
    parser.add_argument('expression', type=str, default='',
                        help="Python expression to be used to transform a row. Specific "
                             "columns can be referred as a fields of of dictionary named r")
    parser.add_argument('file', nargs='?', help='File to read input from. stdin is used by default')

    args = parser.parse_args()
    return args


main()
