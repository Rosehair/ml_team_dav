"""read_csv implemented by Vardges"""
from pandas import DataFrame
import pandas as pd


def read_csv(filename):
    """
    :param filename: file path to read
    :return: dataframe created form file
    """
    with open(filename, 'r') as line:
        content = line.readlines()
    content = [x.strip() for x in content]

    labels = content[0].split(',')
    rows = []
    for index in range(1, len(content)):
        my_dict = {}
        features = (content[index].split(','))
        for step, feature in enumerate(features):
            my_dict.update({labels[step]: int(feature)})
        rows.append(my_dict)
    return DataFrame(rows)


def test(file):
    """
    :param file: path to file to read 
    :return: nothing
    tests if read_csv returned dataframe with the same number of axes and dimensions
    """
    df = read_csv(file)
    df_pandas = pd.read_csv(file)
    if len(df.axes) != len(df_pandas.axes) or df.ndim != df_pandas.ndim:
        print("error!")
    else:
        print("test passed")

test('SPECTF.dat')
