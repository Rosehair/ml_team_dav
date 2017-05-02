"""implementation for random forest by by Vardges Mambreyan"""
import math as math
from collections import Counter
from decision_tree import DecisionTree
import numpy as np


class RandomForest(object):
    """class for Random forest"""
    def __init__(self, num_trees, max_tree_depth, ratio_per_tree=0.25):
        """"
        initialisation for Random forest, 
        sets number of tree, max depth and ratio per tree
        """

        self.num_trees = num_trees
        self.max_tree_depth = max_tree_depth
        self.ratio = ratio_per_tree
        self.trees = None

    def fit(self, data):
        """"fits the data to the forest"""
        trees = []
        sample_size = math.floor(self.ratio * len(data))
        for step in range(self.num_trees):
            number = data.shape[0]
            idx = np.arange(number)
            np.random.seed(step)
            np.random.shuffle(idx)
            data = data[idx]
            data = data[:sample_size, :]
            data = np.array(data)
            tree = DecisionTree(self.max_tree_depth)
            tree.fit(data)
            trees.append(tree)
        self.trees = trees

    def predict(self, data):
        """
        predicts the labels for the data provided, 
        it requires for method fit to be called previously
        """

        labels = []

        def predict(current_tree, datum):
            """predict function to predict outcome for single datum"""
            if current_tree.is_leaf:
                key = max(current_tree.current_results, key=current_tree.current_results.get)
                return key
            if datum[current_tree.column] >= current_tree.value:
                current_tree = current_tree.true_branch
                return predict(current_tree, datum)
            else:
                current_tree = current_tree.false_branch
                return predict(current_tree, datum)

        for data in data:
            prediction = []
            for tree in self.trees:
                prediction.append(predict(tree.tree, data))
            prediction = np.array(prediction)
            count = Counter(prediction)
            labels.append(count.most_common(1)[0][0])

        return labels
