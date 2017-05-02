from decision_tree import DecisionTree
import numpy as np
import math as math
from collections import Counter


class RandomForest(object):

    def __init__(self, num_trees, max_tree_depth, ratio_per_tree=0.25):
        self.num_trees = num_trees
        self.max_tree_depth = max_tree_depth
        self.ratio = ratio_per_tree
        self.trees = None

    def fit(self, data):
        trees = []
        sample_size = math.floor(self.ratio * len(data))
        for s in range(self.num_trees):
            n, d = data.shape
            idx = np.arange(n)
            np.random.seed(s)
            np.random.shuffle(idx)
            data = data[idx]
            data = data[:sample_size, :]
            data = np.array(data)
            tree = DecisionTree(self.max_tree_depth)
            tree.fit(data)
            trees.append(tree)
        self.trees = trees

    def predict(self, X):
        Y = []

        def predict(tree, x):
            if tree.is_leaf:
                key = max(tree.current_results, key=tree.current_results.get)
                return key
            if x[tree.column] >= tree.value:
                tree = tree.true_branch
                return predict(tree, x)
            else:
                tree = tree.false_branch
                return predict(tree, x)

        for x in X:
            prediction = []
            for tree in self.trees:
                # print(predict_x(tree, x))
                prediction.append(predict(tree.tree, x))
            prediction = np.array(prediction)
            count = Counter(prediction)
            Y.append(count.most_common(1)[0][0])

        return Y
