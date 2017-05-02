from collections import defaultdict
import numpy as np


class DecisionNode(object):

    def __init__(self,
                 column=None,
                 value=None,
                 false_branch=None,
                 true_branch=None,
                 current_results=None,
                 is_leaf=False,
                 results=None):
        self.column = column
        self.value = value
        self.false_branch = false_branch
        self.true_branch = true_branch
        self.current_results = current_results
        self.is_leaf = is_leaf
        self.results = results


def dict_of_values(data):
    results = defaultdict(int)
    for row in data:
        r = row[len(row) - 1]
        results[r] += 1
    return dict(results)


def divide_data(data, feature_column, feature_val):
    data1, data2 = [], []
    for example in data:
        if example[feature_column] >= feature_val:
            data1.append(example)
        else: data2.append(example)

    return data1, data2


def gini_impurity(data1, data2):

    N1, N2 = len(data1), len(data2)
    dict1, dict2 = dict_of_values(data1), dict_of_values(data2)

    gini1 = N1*sum((value/N1)*(1 - value/N1) for row, value in dict1.items())
    gini2 = N2*sum((value/N2)*(1 - value/N2) for row, value in dict2.items())

    return gini1 + gini2


def build_tree(data, current_depth=0, max_depth=1e10):

    if len(data) == 0:
        return DecisionNode(is_leaf=True)

    if current_depth == max_depth:
        return DecisionNode(current_results=dict_of_values(data), is_leaf=True)

    if len(dict_of_values(data)) == 1:
        return DecisionNode(current_results=dict_of_values(data), is_leaf=True)

    self_gini = gini_impurity(data, [])
    best_gini = 1e10
    best_column = None
    best_value = None
    best_split = None

    features = [[row[i] for row in data] for i in range(len(data[0]) - 1)]
    features = np.array(features)
    for index, feature in enumerate(features):
        feature = np.unique(feature)
        min = np.amin(feature)
        max = np.amax(feature)
        dif = max - min
        feature = np.array([min+5, min+dif, max-dif, max-5])
        for value in feature:
            data1, data2 = divide_data(data, index, value)
            gini = gini_impurity(data1, data2)
            if gini < best_gini:
                best_gini = gini
                best_column = index
                best_value = value
                best_split = data1, data2

    if abs(self_gini - best_gini) < 1e-10:
        return DecisionNode(current_results=dict_of_values(data), is_leaf=True)
    else:
        return DecisionNode(column=best_column, value=best_value,
                 false_branch= build_tree(best_split[1], current_depth+1, max_depth),
                 true_branch= build_tree(best_split[0], current_depth+1, max_depth),
                 current_results=dict_of_values(data))



