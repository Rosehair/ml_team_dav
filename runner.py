"""
runner file for running the program
it will calculate mean error and std for each
of methods: decision tree, random forest, logistic regression
"""
import math as math
import numpy as np
from decision_tree import DecisionTree
from random_forest import RandomForest
from gradient_descent import gradient_descent, gradient_predict


def accuracy_score(y_true, y_predict):
    """calculates the accuracy score of the method"""
    true = 0
    for index, label in enumerate(y_true):
        if label[0] == y_predict[index]:
            true += 1
    accuracy = 100 * true/len(y_predict)

    return accuracy


def evaluate_performance():
    """
    reads the data and then call each of the method for learning
    will perform evaluation 20 times and will take mean values of them
    """
    filename = './data/SPECTF.dat'
    data = np.loadtxt(filename, delimiter=',')
    data = np.array(data)

    x_data = data[:, 1:]
    y_data = np.array([data[:, 0]]).T
    accuracy_tree = []
    accuracy_forest = []
    accuracy_log = []
    number = x_data.shape[0]
    number_to_split = math.floor(0.7 * len(y_data))
    for trial in range(20):
        idx = np.arange(number)
        np.random.seed(trial)
        np.random.shuffle(idx)
        x_data = x_data[idx]
        y_data = y_data[idx]
        x_data = np.array(x_data)
        data = np.concatenate((x_data, y_data), axis=1)
        data = np.array(data)

        train = data[:number_to_split, :]

        xtest = x_data[number_to_split:, :]
        # test on remaining instances
        ytest = y_data[number_to_split:, :]

        x_log = x_data[:number_to_split, :]
        y_log = y_data[:number_to_split, :]
        # train the decision tree
        classifier = DecisionTree(100)
        classifier.fit(train)
        # output predictions on the remaining data
        y_pred = classifier.predict(xtest)

        # train the Random forest
        classifier_forest = RandomForest(20, 4, 0.4)
        classifier_forest.fit(train)
        # output predictions on the remaining data
        y_pred_forest = classifier_forest.predict(xtest)

        # train the gradient decent
        ones = np.array(np.ones(x_log.shape[0]).reshape(x_log.shape[0], 1))
        x_log = np.concatenate((ones, x_log), axis=1)
        beta = gradient_descent(x_log, y_log)
        ones1 = np.array(np.ones(xtest.shape[0]).reshape(xtest.shape[0], 1))
        xtest = np.concatenate((ones1, xtest), axis=1)
        y_predict_log = gradient_predict(xtest, beta)
        # output predictions on the remaining data

        accuracy_tree.append(accuracy_score(ytest, y_pred))
        accuracy_forest.append(accuracy_score(ytest, y_pred_forest))
        y_log_test = []
        for step in range(ytest.shape[0]):
            if ytest[step] == 0:
                y_log_test.append([-1])
            else:
                y_log_test.append([1])
        accuracy_log.append(accuracy_score(np.array(y_log_test), y_predict_log))
        print('step', trial)


    # compute the training accuracy of the model
    meanDecisionTreeAccuracy = np.mean(accuracy_tree)
    stddevDecisionTreeAccuracy = np.std(accuracy_tree)
    meanLogisticRegressionAccuracy = np.mean(accuracy_log)
    stddevLogisticRegressionAccuracy = np.std(accuracy_log)
    meanRandomForestAccuracy = np.mean(accuracy_forest)
    stddevRandomForestAccuracy = np.std(accuracy_forest)

    # make certain that the return value matches the API specification
    stats = np.zeros((3, 3))
    stats[0, 0] = meanDecisionTreeAccuracy
    stats[0, 1] = stddevDecisionTreeAccuracy
    stats[1, 0] = meanRandomForestAccuracy
    stats[1, 1] = stddevRandomForestAccuracy
    stats[2, 0] = meanLogisticRegressionAccuracy
    stats[2, 1] = stddevLogisticRegressionAccuracy
    return stats


if __name__ == "__main__":
    statistics = evaluate_performance()
    print("Decision Tree Accuracy = ", statistics[0, 0], " (", statistics[0, 1], ")")
    print("Random Forest Tree Accuracy = ", statistics[1, 0], " (", statistics[1, 1], ")")
    print("Logistic Reg. Accuracy = ", statistics[2, 0], " (", statistics[2, 1], ")")

