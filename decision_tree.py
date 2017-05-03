import numpy as np


class DecisionTree(object):
    """
    DecisionTree class, that represents one Decision Tree

    :param max_tree_depth: maximum depth for this tree.
    """
    def __init__(self, max_tree_depth):
        self.max_depth = max_tree_depth
        self.tree = None

    class Condition:
        def __init__(self, feature=None, value=None):
            self.feature = feature
            self.value = value

        def check(self, x):
            return x[self.feature] > self.value

    class Node:
        def __init__(self, node_true=None, node_false=None, condition=None,
                     label=None, label_dict=None, is_leaf=False, depth=-1):
            self.node_true = node_true
            self.node_false = node_false
            self.condition = condition
            self.label = label
            self.label_dict = label_dict
            self.is_leaf = is_leaf
            self.depth = depth

    def fit(self, X, y):
        """
        :param X: 2 dimensional python list or numpy 2 dimensional array
        :param y: 1 dimensional python list or numpy 1 dimensional array
        """

        self.tree = self.build_tree(X, y)

    @staticmethod
    def get_label(y):
        return np.argmax(np.bincount(y.astype(dtype=int)))

    @staticmethod
    def get_label_dict(y):
        bc = np.bincount(y.astype(dtype=int))
        bc = np.column_stack((np.arange(len(bc)), bc))
        bc = bc[bc[:, 1] > 0]
        bc = {d[0]: d[1] for d in bc}
        return bc

    @staticmethod
    def split_data(X, y, condition):
        x_false = []
        x_true = []
        y_false = []
        y_true = []
        for (x, y) in zip(X, y):
            if condition.check(x) and True:
                x_true.append(x)
                y_true.append(y)
            else:
                x_false.append(x)
                y_false.append(y)
        x_false = np.array(x_false)
        x_true = np.array(x_true)
        y_false = np.array(y_false, dtype=int)
        y_true = np.array(y_true, dtype=int)
        # print("SPLIT DATA: ", len(y_true), len(y_false),condition.feature, condition.value)
        return x_true, y_true, x_false, y_false

    @staticmethod
    def calc_gini_one(y):
        N = len(y)
        bincount_y = np.bincount(y) / N
        return N * np.sum(bincount_y * (1 - bincount_y))

    @staticmethod
    def calc_gini(y1, y2):
        # N1*sum(p_k1 * (1-p_k1)) + N2*sum(p_k2 * (1-p_k2))
        return DecisionTree.calc_gini_one(y1) + \
               + DecisionTree.calc_gini_one(y2)

    def build_tree(self, X, y, current_depth=0):
        y = np.array(y, dtype=int)
        if current_depth == self.max_depth:
            return DecisionTree.Node(is_leaf=True, label=DecisionTree.get_label(y),
                                     label_dict=DecisionTree.get_label_dict(y), depth=current_depth)

        if len(np.unique(y)) <= 1:
            return DecisionTree.Node(is_leaf=True, label=DecisionTree.get_label(y),
                                     label_dict=DecisionTree.get_label_dict(y), depth=current_depth)

        best_gini = 10000
        best_condition = None
        best_split = None

        def update_best(condition):
            x_true, y_true, x_false, y_false = DecisionTree.split_data(X, y, condition)
            if len(y_true) == 0 or len(y_false) == 0:
                return False

            nonlocal best_gini, best_condition, best_split

            gini = DecisionTree.calc_gini(y_true, y_false)
            if gini < best_gini:
                best_gini = gini
                best_condition = condition
                best_split = ((x_true, y_true), (x_false, y_false))
                return True
            return False

        for feature in range(X.shape[1]):
            candidates = np.unique(X[:, feature])
            candidates = (candidates[1:] + candidates[0:-1]) / 2
            # np.random.shuffle(candidates)
            for candidate in candidates:
                condition = DecisionTree.Condition(feature, candidate)
                update_best(condition)
        if best_split is None:
            return DecisionTree.Node(is_leaf=True, label=DecisionTree.get_label(y),
                                     label_dict=DecisionTree.get_label_dict(y), depth=current_depth)
        node_true = DecisionTree.build_tree(self, *best_split[0], current_depth=current_depth + 1)
        node_false = DecisionTree.build_tree(self, *best_split[1], current_depth=current_depth + 1)

        return DecisionTree.Node(node_true, node_false, best_condition, label=DecisionTree.get_label(y),
                                 label_dict=DecisionTree.get_label_dict(y), depth=current_depth)
    @staticmethod
    def print_tree(tree, indent=''):

        if tree.is_leaf:
            print(str(tree.label) + " : " + str(tree.label_dict))
        else:
            # Print the criteria
            #         print (indent+'Current Results: ' + str(tree.current_results))
            print('Column ' + str(tree.condition.feature) + ' : ' + str(tree.condition.value) + '?  ' +
                  "Labels: " + str(tree.label_dict) + " depth: " + str(tree.depth))

            # Print the branches
            print(indent + 'True->', end="")
            DecisionTree.print_tree(tree.node_true, indent + '  ')
            print(indent + 'False->', end="")
            DecisionTree.print_tree(tree.node_false, indent + '  ')

    def print(self):
        DecisionTree.print_tree(self.tree)

    @staticmethod
    def predict_tree(tree, x):
        assert tree is not None
        if tree.is_leaf:
            return tree.label
        if tree.condition.check(x):
            return DecisionTree.predict_tree(tree.node_true, x)
        return DecisionTree.predict_tree(tree.node_false, x)

    def predict(self, X):
        return np.array([DecisionTree.predict_tree(self.tree, x) for x in X])
