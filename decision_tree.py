"""implementation for desicion tree by Vardges Mmbreyan"""
from utils import build_tree


class DecisionTree(object):
    """decision tree object"""
    def __init__(self, max_tree_depth):
        self.max_depth = max_tree_depth

    def fit(self, data):
        """ft the data to tree"""
        tree = build_tree(data, max_depth=self.max_depth)
        self.tree = tree

    def predict(self, data):
        """predicts the data with decision tree"""
        labels = []

        def predict_x(current_tree, datum):
            """predict the outcome of single datum"""
            if current_tree.is_leaf:
                return list(current_tree.current_results)[0]
            if datum[current_tree.column] >= current_tree.value:
                current_tree = current_tree.true_branch
                return predict_x(current_tree, datum)
            else:
                current_tree = current_tree.false_branch
                return predict_x(current_tree, datum)

        for datum in data:
            tree = self.tree
            labels.append(predict_x(tree, datum))

        return labels
