"""
Decision tree classifier implementation
"""

from collections import defaultdict

import numpy as np


class DecisionNode(object):
    """
    Decision Node instance
    """

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


def pred(tree, sample):
    """

    :param tree: type DecisionNode
    :param sample: 1 d numpy array
    :return:
    """
    if len(tree.current_results) == 1 or tree.is_leaf:
        return max(tree.current_results, key=tree.current_results.get)
    else:
        if sample[tree.column] >= tree.value:
            return pred(tree.true_branch, sample)
        else:
            return pred(tree.false_branch, sample)


def dict_of_values(data):
    """

    :param data:
    :return:
    """
    results = defaultdict(int)
    for row in data:
        r = row[len(row) - 1]
        results[r] += 1
    return dict(results)


def divide_data(data, feature_column, feature_val):
    """

    :param data:
    :param feature_column:
    :param feature_val:
    :return:
    """
    data1, data2 = [], []
    for example in data:
        if example[feature_column] >= feature_val:
            data1.append(example)
        else:
            data2.append(example)
    return data1, data2


def gini_impurity(data1, data2):
    """

    :param data1:
    :param data2:
    :return:
    """
    len1, len2 = len(data1), len(data2)
    dict1, dict2 = dict_of_values(data1), dict_of_values(data2)

    gini1 = len1 * sum((value / len1) * (1 - value / len1) for row, value in dict1.items())
    gini2 = len2 * sum((value / len2) * (1 - value / len2) for row, value in dict2.items())
    return gini1 + gini2


def build_tree(data, current_depth=0, max_depth=1e10):
    """

    :param data:
    :param current_depth:
    :param max_depth:
    :return:
    """
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

    features = np.array([[row[i] for row in data] for i in range(len(data[0]) - 1)])

    for index, feature in enumerate(features):
        feature = np.unique(feature)
        # feature = np.percentile(feature, np.arange(0, 100, 25))
        feature = [np.percentile(feature, i) for i in np.arange(0, 101, 25)]

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
                            false_branch=build_tree(best_split[1], current_depth + 1, max_depth),
                            true_branch=build_tree(best_split[0], current_depth + 1, max_depth),
                            current_results=dict_of_values(data))


class DecisionTree(object):
    """
    DecisionTree class, that represents one Decision Tree

    :param max_tree_depth: maximum depth for this tree.
    """

    def __init__(self, max_tree_depth):
        self.max_depth = max_tree_depth
        self.tree = None

    def fit(self, train_data, train_labels):
        """
        :param train_data: 2 dimensional python list or numpy 2 dimensional array
        :param train_labels: 1 dimensional python list or numpy 1 dimensional array
        """
        train_labels = np.reshape(train_labels, (np.size(train_labels), 1))
        data = np.concatenate((train_data, train_labels), axis=1)
        self.tree = build_tree(data, max_depth=self.max_depth)

    def predict(self, predict_data):
        """
        :param predict_data: 2 dimensional python list or numpy 2 dimensional array
        :return: Y - 1 dimension python list with labels
        """
        return np.array([np.array([pred(self.tree, x)]) for x in predict_data])
