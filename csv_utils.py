"""
Module is to read csv files
"""
import numpy as np

def read_csv(path, delimiter=','):
    """
    :param path: the path of the csv file
    :param delimiter: the delimiter
    :return: the object data the csv stored to
    """
    with open(path, 'r') as csv:
        read_data = csv.read().split('\n')
    header = read_data[0].split(delimiter)
    data = read_data[1: ]
    body = []
    for row in data:
        if len(row) is 0:
            break
        else:
            body.append([float(x) if '.' in x else int(x) for x in row.split(delimiter)])
    body = np.array(body).T
    print header
    res = {}
    for ind, name in enumerate(header):
        res[name] = body[ind, :]
    return res

def test(dataframe, res):
    """
    :param dataframe: dataframe to compare with
    :param res: our function's output object
    :return: True if the data is same
    """
    for col in dataframe.columns:
        if not np.array_equal(dataframe[col].values, res[col]):
            return False
    return True
