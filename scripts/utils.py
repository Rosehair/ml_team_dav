import sys


def find_features(string_f, labels, unique=False, complement=False):
    """
    :param complement: return indexes of elements that are not in fields
    :param unique: to take only unique fields
    :param string_f: feature string
    :param labels: first row of the data
    :return: indexes of feature ti be shown
    """

    if len(string_f) == 0:
        indexes = []
    else:
        features = string_f.split(',')
        if unique:
            features = list(set(features))

        if len(set(labels) - set(features)) != len(labels):
            indexes = [labels.index(feature) for feature in features]
        else:
            indexes = []

        if complement:
            label_indexes = [labels.index(label) for label in labels]
            indexes = list(set(label_indexes) - set(indexes))

    if len(indexes) == 0:
        report_wrong_fields_to_cut(string_f)
        return False
    return indexes


def filter_by_column(row, indexes, args=None):
    """
    :param row: original rows of file
    :param indexes: indexes to only show in the end
    :return: new row
    """
    new_row = []
    if len(row) - 1 < max(indexes):
        report_wrong_number_of_columns(row, args.careful, args.quiet)
    else:
        for index in indexes:
            new_row.append(row[index])
    return new_row


# error handling
class InputError(Exception):
    """Exception raised for errors in the input.
    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


    def __repr__(self):
        return self.expression + ' ' + self.message

def report_error(error, quiet=False):
    """
    Formats the error message and prints it to stderr
    :param error: string containing error text
    :param quiet: if True, don't report errors
    """
    if not quiet:
        sys.stderr.write('ERROR: ' + error + '\n')


def report_wrong_number_of_columns(row, careful=False, quiet=False):
    """
    Reports invalid columns in a row error
    :param row: row which is invalid
    :param careful: whether to ignore this kind of error
    :param quiet: whether to print the error message to stderr
    """
    error = 'Wrong number of columns in row'
    if careful:
        raise InputError(row, error)
    report_error(error + '"' + ','.join(row) + '"', quiet)


def report_wrong_fields_to_cut(fields, careful=False, quiet=False):
    """
    Reports that invalid fields are given to csvcut
    :param fields: fields string which is invalid
    :param careful: whether to ignore this kind of error
    :param quiet: whether to print the error message to stderr
    """
    error = 'Empty or non existing fields: '
    if careful:
        raise InputError(fields, error)
    report_error(error + fields, quiet)


def report_wrong_expression(expression, careful=False, quiet=False):
    """
    Reports that invalid fields are given to csvcut
    :param expression: expression by user which is invalid
    :param careful: whether to ignore this kind of error
    :param quiet: whether to print the error message to stderr
    """
    error = 'Invalid expression  or non existing column name for map in: '
    if careful:
        raise InputError(expression, error)
    report_error(error + expression, quiet)


def report_wrong_exec(expression, careful=False, quiet=False):
    """
    Reports that invalid fields are given to csvcut
    :param expression: expression by user which is invalid
    :param careful: whether to ignore this kind of error
    :param quiet: whether to print the error message to stderr
    """
    error = 'Invalid EXEC to execute before map: '
    if careful:
        raise InputError(expression, error)
    report_error(error + expression, quiet)

