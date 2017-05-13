from argparse import ArgumentParser
import operator
import csv
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, '..')))
from scripts.utils import Raise, InputError, report_error

DESCRIPTION = 'csvjoin.py - Join two csv files using the keys provided.'
EXAMPLES = 'examples: csvjoin.py stat1.txt stat2.txt -k id, -t OUTER'

def function_csvjoin(args):
    try:
        if args.keys == '':
            raise InputError('Key error','key field is empty')
        if args.file is None:
            Raise(InputError('File error', 'input file is required'),careful=True)
        if args.file2 is None:
            args.file2 = args.file
            input_file = sys.stdin
            Raise(InputError('File error', 'input file is required'))
        else:
            input_file = open(args.file)

        input_file2 = open(args.file2)
        output_stream = open(args.output_file, 'w') if args.output_file else sys.stdout
        keys = args.keys.strip().split(args.separator)

        headline_str = input_file.readline()
        headline = headline_str.strip().split(args.separator)
        headline_n = {i: k for i, k in enumerate(headline)}
        headline = {k: i for i, k in enumerate(headline)}
        if all(map(lambda x: x.isdigit() or x == '-', keys)):
            _keys = []
            for key in keys:
                key = int(key)
                try:
                    _keys.append(headline_n[key])
                except KeyError as err:
                    Raise(InputError('Key error', '{} key out of range (hint: column numbers start from zero)'.format(err.args[0])),
                          careful=args.careful, quiet=args.quiet)
        else:
            _keys = []
            for key in keys:
                try:
                    _keys.append(headline[key])
                except KeyError as err:
                    Raise(InputError('Key error', '{} not found'.format(err.args[0])),
                          careful=args.careful, quiet=args.quiet)

        if len(_keys) == 0:
            Raise(InputError('Key error', 'You should provide valid keys'), careful=True, quiet=args.quiet)
        keys = _keys

        headline_str2 = input_file2.readline()
        headline2 = headline_str2.strip().split(args.separator)
        headline2_n = {i: k for i, k in enumerate(headline2)}
        headline2 = {k: i for i, k in enumerate(headline2)}
        for i, key in enumerate(keys):
            if headline2.get(headline_n[key],None) is None:
                Raise(InputError('Key error','kes mismatch'),careful=args.careful,quiet=args.quiet)
                keys.pop(i)
        L = []

        writer = csv.writer(output_stream, delimiter=args.separator, lineterminator='\n')
        writer.writerow([headline_n[key] for key in keys])

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
    except InputError as err:
        report_error(err.message)
    except FileNotFoundError:
        report_error("File {} doesn't exist".format(args.file))
    except KeyError:
        report_error('You should provide valid keys')
    except KeyboardInterrupt:
        pass
    except BrokenPipeError:
        # The following line prevents python to inform you about the broken pipe
        sys.stderr.close()
    # except Exception as e:
    #     report_error('Caught unknown exception. Please report to developers: {}'.format(e))
    finally:
        try:
            input_file.close()
            input_file2.close()
            output_stream.close()
        except:
            pass



def parse_args():
    parser = ArgumentParser(description=DESCRIPTION, epilog=EXAMPLES)
    parser.add_argument('-n', '--number_of_lines', type=int, help='Number of last rows to print if positive '
                                                                  'NUMBER_OF_LINES. Else skips NUMBER_OF_LINES lines '
                                                                  'and prints till the end of input. Default 10.',
                        default=10)
    parser.add_argument('-o', '--output_file', type=str, help='Output file. stdout is used by default')
    parser.add_argument('-q', '--quiet',action='store_true', help='Don\'t print information regarding errors')
    parser.add_argument('--careful', help='Stop if input contains an incorrect row', action='store_true')
    parser.add_argument('-s', '--separator', type=str, help='Separator to be used', default=',')
    parser.add_argument('-k', '--keys', type=str, default='', help='Comma-separated list of columns to be used as reduce keys. Column names or column numbers can be used here. These columns will be used as the join keys.')
    parser.add_argument('-c', '--conflict_prefix', type=str, help='Specify a prefix to be used for the columns taken from file2 having the same names. Default is \'conflict_\'.', default='conflict_')
    parser.add_argument('-t', '--type', type=str, help='Type of join to be used. Either INNER, LEFT or OUTER. INNER is default.')
    parser.add_argument('file', nargs='?', help='File to read input from. stdin is used by default')
    parser.add_argument('file2', nargs='?', help='File to join with')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    function_csvjoin(parse_args())