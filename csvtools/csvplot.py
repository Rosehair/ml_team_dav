#!/home/david/miniconda3/bin/python3
import sys
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from utils import *

DESCRIPTION = 'csvplot - plots the data from csv file'
EXAMPLE = 'csvplot -y count example.txt'


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('-s', '--separator', type=str, help='separator to be used', default=',')
    parser.add_argument('-o', '--output_file', type=str, help='output file. stdout is used by default')
    parser.add_argument('-x', type=str, help='specify key to iterate over x axes')
    parser.add_argument('-y', type=str, help='specify columns to be plotted')
    parser.add_argument('--xlabel', type=str, help='label for x axis')
    parser.add_argument('--ylabel', type=str, help='label for y axis')

    parser.add_argument('file', nargs='?', help='File to read input from. stdin is used by default')
    return parser.parse_args()


def main():
    args = parse_arguments()
    print(args)
    input_stream = open(args.file, 'r') if args.file else sys.stdin
    output_stream = open(args.output_file, 'w') if args.output_file else sys.stdout

    first_row = input_stream.readline().strip().split(args.separator)
    x_index = find_features(args.x, first_row) if args.x else None
    y_index = find_features(args.y, first_row)

    row_num = 0
    x_points = []
    y_points = []
    while True:
        row_data = input_stream.readline()
        if len(row_data):
            row = row_data.strip().split(args.separator)
            x_points.append(row_num if not x_index else filter_by_column(row, x_index))
            y_points.append(filter_by_column(row, y_index))
            row_num += 1
        else:
            break

    plt.plot(x_points, y_points)
    if args.xlabel:
        plt.xlabel(args.xlabel)
    if args.ylabel:
        plt.ylabel(args.ylabel)
    plt.show()

    if input_stream != sys.stdin:
        input_stream.close()
    if output_stream != sys.stdout:
        output_stream.close()


main()
