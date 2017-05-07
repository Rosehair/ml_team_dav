from decision_tree import DecisionTree
import numpy as np


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
        self.ratio = ratio_per_tree
        self.trees = None

    def fit(self, X, y):
        """
        :param X: 2 dimensional python list or numpy 2 dimensional array
        :param y: 1 dimensional python list or numpy 1 dimensional array
        """
        self.trees = []
        for _ in range(self.num_trees):
            perm = np.random.permutation(len(X))[0:int(len(X)*self.ratio)]
            current_X = X[perm]
            current_y = y[perm]
            self.trees.append(DecisionTree(self.max_tree_depth))
            self.trees[-1].fit(current_X, current_y)

    def predict(self, X):
        """
        :param X: 2 dimensional python list or numpy 2 dimensional array
        :return: (Y, conf), tuple with Y being 1 dimension python
        list with labels, and conf being 1 dimensional list with
        confidences for each of the labels.
        """
        ys = np.array([tree.predict(X) for tree in self.trees])
        trees = self.num_trees*1.

        y_mean = ys.mean(axis=0)
        y_ones = np.sum(ys, axis=0)
        conf = []
        y = []
        for y_mean, y_ones in zip(y_mean, y_ones):
            y_mean = 1 if y_mean > 0.5 else 0
            if y_mean == 1:
                conf.append(y_ones/trees)
            else:
                conf.append(1 - y_ones/trees)
            y.append(y_mean)
        return np.array(y), np.array(conf)
