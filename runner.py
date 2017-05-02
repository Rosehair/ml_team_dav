import numpy as np
from decision_tree import DecisionTree
import math as math
from random_forest import RandomForest
from logistic_regression import gradient_descent, gradient_predict


def accuracy_score(Y_true, Y_predict):
    true = 0
    for i, y in enumerate(Y_true):
        if y[0] == Y_predict[i]: true += 1

    accuracy = 100 * true/len(Y_predict)

    return accuracy


def evaluate_performance():

    filename = 'SPECTF.dat'
    data = np.loadtxt(filename, delimiter=',')
    data = np.array(data)

    X = data[:, 1:]
    Y = np.array([data[:, 0]]).T
    # data = np.concatenate((X, Y), axis=1)
    accuracy_tree = []
    accuracy_forest = []
    accuracy_log = []
    n, d = X.shape
    number_to_split = math.floor(0.7 * len(Y))
    for trial in range(20):
        idx = np.arange(n)
        np.random.seed(trial)
        np.random.shuffle(idx)
        X = X[idx]
        Y = Y[idx]
        X = np.array(X)
        X_log = X
        data = np.concatenate((X, Y), axis=1)
        data = np.array(data)

        train = data[:number_to_split, :]

        Xtest = X[number_to_split:, :]
        # test on remaining instances
        ytest = Y[number_to_split:, :]

        X_log = X[:number_to_split, :]
        Y_log = Y[:number_to_split, :]
        # train the decision tree
        classifier = DecisionTree(100)
        classifier.fit(train)
        # output predictions on the remaining data
        y_pred = classifier.predict(Xtest)

        # train the decision tree
        classifier_forest = RandomForest(20, 4, 0.4)
        classifier_forest.fit(train)
        # output predictions on the remaining data
        y_pred_forest = classifier_forest.predict(Xtest)

        # train the decision tree
        ones = np.array(np.ones(X_log.shape[0]).reshape(X_log.shape[0], 1))
        X_log = np.concatenate((ones,X_log), axis=1)
        beta = gradient_descent(X_log, Y_log)
        ones1 = np.array(np.ones(Xtest.shape[0]).reshape(Xtest.shape[0], 1))
        Xtest = np.concatenate((ones1, Xtest), axis=1)
        y_predict_log = gradient_predict(Xtest, beta)
        # output predictions on the remaining data



        accuracy_tree.append(accuracy_score(ytest, y_pred))
        accuracy_forest.append(accuracy_score(ytest, y_pred_forest))
        y_log_test = []
        for s in range(ytest.shape[0]):
            if ytest[s] == 0: y_log_test.append([-1])
            else: y_log_test.append([1])
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


# Do not modify from HERE...
if __name__ == "__main__":
    stats = evaluate_performance()
    print("Decision Tree Accuracy = ", stats[0, 0], " (", stats[0, 1], ")")
    print("Random Forest Tree Accuracy = ", stats[1, 0], " (", stats[1, 1], ")")
    print("Logistic Reg. Accuracy = ", stats[2, 0], " (", stats[2, 1], ")")
# ...to HERE.
