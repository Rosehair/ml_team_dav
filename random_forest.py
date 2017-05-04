"""
Random forest classifier implementation
"""
import math
from time import time

import numpy as np

from decision_tree import DecisionTree


class RandomForest(object):
    """
    RandomForest a class, that represents Random Forests.

    :param num_trees: Number of trees in the random forest
    :param max_tree_depth: maximum depth for each of the trees in the forest.
    :param ratio_per_tree: ratio of points to use to train each of
        the trees.
    """

    def __init__(self, num_trees, max_tree_depth, ratio_per_tree=0.5):
        self.num_trees = num_trees
        self.max_tree_depth = max_tree_depth
        self.ratio_per_tree = ratio_per_tree
        self.trees = None

    def fit(self, train_data, label_data):
        """
        :param train_data: 2 dimensional python list or numpy 2 dimensional array
        :param label_data: 1 dimensional python list or numpy 1 dimensional array
        """
        self.trees = []

        for _ in range(0, self.num_trees):
            seed = int(math.floor(time() / 150))
            idx = np.arange(np.size(train_data, axis=0))
            np.random.seed(seed)
            np.random.shuffle(idx)
            train_data = train_data[idx]
            label_data = label_data[idx]

            train_part = np.int(self.ratio_per_tree * np.size(train_data, axis=0))
            x_train = train_data[1:train_part, :]
            y_train = label_data[1:train_part, :]

            curr = DecisionTree(self.max_tree_depth)
            curr.fit(x_train, y_train)
            self.trees.append(curr)

    def predict(self, predict_data):
        """
        :param predict_data: 2 dimensional python list or numpy 2 dimensional array
        :return: (Y, conf), tuple with Y being 1 dimension python
        list with labels, and conf being 1 dimensional list with
        confidences for each of the labels.
        """
        predictions = np.array([tree.predict(predict_data) for tree in self.trees])
        predictions = np.swapaxes(predictions, 0, 1)
        return np.array([most_frequent(yi) for yi in predictions])


def most_frequent(arr):
    """
    Auxiliary function to get frequency of repeated value
    :param arr: 1 dimensional array
    :return: the most frequent element
    """
    arr = arr.flatten().astype(int)
    ans = np.argmax(np.bincount(arr))
    return ans
