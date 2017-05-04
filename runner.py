"""
This file is for running random forest classifier on our data
"""
import math
from time import time

import numpy as np

from decision_tree import DecisionTree
from logistic_regression import gradient_descent, sigmoid
from random_forest import RandomForest


def accuracy_score(y_true, y_predict):
    """

    :param y_true: true labels of given data
    :param y_predict: predicted labels of given data
    :return:
    """
    y_true = y_true.flatten()
    y_predict = y_predict.astype(float).flatten()
    t_sum = sum([1 if y_true[i] == y_predict[i] else 0 for i in range(0, np.size(y_true))]) + .0
    return t_sum / np.size(y_true)


def recall(y_true, y_predict):
    """

    :param y_true: true labels of given data
    :param y_predict: predicted labels of given data
    :return:
    """
    y_true = y_true.flatten()
    y_predict = y_predict.astype(float).flatten()
    true_pos = .0
    for i in range(0, np.size(y_true)):
        if y_true[i] == y_predict[i] and y_predict[i] == 0:
            true_pos += 1
    return true_pos / np.sum(np.abs(1 - y_true))


def evaluate_performance():
    """
    Evaluate the performance of decision trees and logistic regression,
    average over 1,000 trials of 10-fold cross validation

    Return:
      a matrix giving the performance that will contain the following entries:
      stats[0,0] = mean accuracy of decision tree
      stats[0,1] = std deviation of decision tree accuracy
      stats[1,0] = mean accuracy of logistic regression
      stats[1,1] = std deviation of logistic regression accuracy

    ** Note that your implementation must follow this API**
    """

    # Load Data
    filename = './SPECTF.dat'
    data = np.loadtxt(filename, delimiter=',')
    x_data = data[:, 1:]
    y_data = np.array([data[:, 0]]).T
    data_len, _ = x_data.shape

    accuracy_list = []
    rf_accuracy = []
    lr_accuracy = []

    for _ in range(10):
        # shuffle
        seed = int(math.floor(time() / 150))
        idx = np.arange(data_len)
        np.random.seed(seed)
        np.random.shuffle(idx)
        x_data = x_data[idx]
        y_data = y_data[idx]

        train_part = np.int(0.8 * np.size(x_data, axis=0))
        x_train = x_data[1:train_part, :]  # train on 90%
        x_test = x_data[train_part:, :]
        y_train = y_data[1:train_part, :]  # test on 10%
        y_test = y_data[train_part:, :]

        xtrainlr = np.concatenate((np.ones(shape=(1, np.shape(x_train)[0])).T, x_train), axis=1)
        xtestlr = np.concatenate((np.ones(shape=(1, np.shape(x_test)[0])).T, x_test), axis=1)

        ytr = 2 * y_train - 1
        yts = 2 * y_test - 1

        beta = gradient_descent(xtrainlr, ytr, max_steps=500, step_size=0.3)
        beta = np.reshape(beta, (1, np.size(beta))).T
        lrres = sigmoid(xtestlr.dot(beta))
        lr_accuracy.append(accuracy_score(yts, lrres))

        random_forest = RandomForest(20, 10, 0.3)
        random_forest.fit(x_train, y_train)
        pred = random_forest.predict(x_test)

        classifier = DecisionTree(10)
        classifier.fit(x_train, y_train)
        y_pred = classifier.predict(x_test)

        rf_acc = accuracy_score(y_test, pred)
        accuracy = accuracy_score(y_test, y_pred)

        rf_accuracy.append(rf_acc)
        accuracy_list.append(accuracy)

        print("DT: ", accuracy, " ", recall(y_test, y_pred),
              " RF: ", rf_acc, " ", recall(y_test, pred))

    accuracy_list = np.array(accuracy_list)
    rf_accuracy = np.array(rf_accuracy)

    mean_decision_tree_accuracy = np.mean(accuracy_list)
    stddev_decision_tree_accuracy = np.std(accuracy_list)
    mean_log_reg_accuracy = np.mean(lr_accuracy)
    stddev_log_reg_accuracy = np.std(lr_accuracy)
    mean_random_forest_accuracy = np.mean(rf_accuracy)
    stddev_random_forest_accuracy = np.std(rf_accuracy)

    # make certain that the return value matches the API specification
    stats = np.zeros((3, 3))
    stats[0, 0] = mean_decision_tree_accuracy
    stats[0, 1] = stddev_decision_tree_accuracy
    stats[1, 0] = mean_random_forest_accuracy
    stats[1, 1] = stddev_random_forest_accuracy
    stats[2, 0] = mean_log_reg_accuracy
    stats[2, 1] = stddev_log_reg_accuracy
    return stats


# Do not modify from HERE...
if __name__ == "__main__":
    res_stats = evaluate_performance()
    print("Decision Tree Accuracy = ", res_stats[0, 0], " (", res_stats[0, 1], ")")
    print("Random Forest Tree Accuracy = ", res_stats[1, 0], " (", res_stats[1, 1], ")")
    print("Logistic Reg. Accuracy = ", res_stats[2, 0], " (", res_stats[2, 1], ")")
# ...to HERE.
