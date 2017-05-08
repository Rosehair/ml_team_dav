def find_features(string_f, labels, unique=False):
    """
    :param unique: to take only unique fields
    :param string_f: feature string
    :param labels: first row of the data
    :return: indexes of feature ti be shown
    """

    if len(string_f) is 0:
        features = []
    else:
        features = string_f.split(',')
        if unique:
            features = list(set(features))
    indexes = []
    for index, label in enumerate(labels):
        for feature in features:
            if label == feature:
                indexes.append(index)
    return indexes


def filter_by_column(row, indexes):
    """
    :param row: original rows of file
    :param indexes: indexes to only show in the end
    :return: new row
    """
    new_row = []
    for index in indexes:
        new_row.append(row[index])
    return new_row
