from dtOmitted import build_tree


class DecisionTree(object):

    def __init__(self, max_tree_depth):
        self.max_depth = max_tree_depth

    def fit(self, data):
        tree = build_tree(data, max_depth=self.max_depth)
        self.tree = tree

    def predict(self, X):
        Y = []

        def predict_x(tree, x):
            if tree.is_leaf:
                return list(tree.current_results)[0]
            if x[tree.column] >= tree.value:
                tree = tree.true_branch
                return predict_x(tree, x)
            else:
                tree = tree.false_branch
                return predict_x(tree, x)

        for x in X:
            tree = self.tree
            Y.append(predict_x(tree, x))

        return Y
