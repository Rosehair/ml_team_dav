def find_features(string_f, labels, unique=False, complement=False):
    """
    :param complement: return indexes of elements that are not in fields
    :param unique: to take only unique fields
    :param string_f: feature string
    :param labels: first row of the data
    :return: indexes of feature ti be shown
    """
    if len(string_f) == 0:
        features = []
    else:
        features = string_f.split(',')
        if unique:
            features = list(set(features))
    indexes = [labels.index(i) for i in features]
    if complement:
        label_indexes = [labels.index(i) for i in labels]
        indexes = list(set(label_indexes) - set(indexes))
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
