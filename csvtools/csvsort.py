from argparse import ArgumentParser
import operator
import csv
import sys
from .utils import InputError, report_wrong_fields_to_cut, Raise, report_error

DESCRIPTION = 'csvtail - Sort the rows of csv stream ascending.'
EXAMPLES = 'examples: cat stat.csv | csvsort -k shows'


BLOCK_SIZE = 1024

def function_csvsort(args):
    try:
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
            _keys = []
            for key in keys:
                try:
                    _keys.append(headline[key])
                except KeyError as err:
                    report_wrong_fields_to_cut(str(err), careful=args.careful, quiet=args.quiet)
                    pass
            if len(_keys) == 0:
                Raise(InputError('Key error', 'You should provide valid keys'),careful=True, quiet=args.quiet)
            keys = _keys
        L = []
        for line in input_stream:
            line = line.strip().split(args.separator)
            if args.numeric:
                for key in keys:
                    try:
                        x = float(line[key])
                        line[key] = int(x) if x.is_integer() else x
                    except ValueError:
                        Raise(InputError('number error','items are not numbers'), careful=True)
            L.append(line)

        print(operator.itemgetter(*keys)(L[1]))

        L.sort(key=operator.itemgetter(*keys), reverse=args.descending)
        writer = csv.writer(output_stream, delimiter=args.separator, lineterminator='\n')
        writer.writerow(headline.keys())
        for line in L:
            writer.writerow(line)
    except FileNotFoundError:
        report_error("File {} doesn't exist".format(args.file))
    except InputError as e:
        print(e.expression + ': ' + e.message)
    except KeyboardInterrupt:
        pass
    except BrokenPipeError:
        # The following line prevents python to inform you about the broken pipe
        sys.stderr.close()
    except Exception as e:
        report_error('Caught unknown exception. Please report to developers: {}'.format(e))
    finally:
        try:
            input_stream.close()
            output_stream.close()
        except:
            pass


def parse_args():
    parser = ArgumentParser(description=DESCRIPTION, epilog=EXAMPLES)
    parser.add_argument('-s', '--separator', type=str, help='Separator to be used', default=',')
    parser.add_argument('-k', '--keys', type=str, help='Specify the list of keys (comma separated) to sort on. Field names or field numbers can be used. Dash can be used to specify fields ranges. Range \'F1-F2\' stands for all fields between F1 and F2. Range \'-F2\' stands for all fields up to F2. Range \'F1-\' stands for all fields from F1 til the end.', default='')
    parser.add_argument('-m', '--max-rows', type=int, help='Don\'t load to memory more than MAX_ROWS rows at a time. This option is crucial if you have to deal with huge csv files. Default value is 0 that meanse that this will sort file in memory.')
    parser.add_argument('-q', '--quiet', help="Don't print information regarding errors", action='store_true')
    parser.add_argument('--careful', help='Stop if input contains an incorrect row', action='store_true')
    parser.add_argument('--descending', action='store_true', help='If provided, perform descending sort instead of ascending')
    parser.add_argument('--numeric', action='store_true', help='If provided, keys will be interpreted as numbers. Otherwise - as strings.')
    parser.add_argument('-o', '--output_file', type=str, help='Output file. stdout is used by default')
    parser.add_argument('file', nargs='?', help='File to read input from. stdin is used by default')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    function_csvsort(parse_args())