import numpy as np
import matplotlib.pyplot as plt

from decision_tree import DecisionTree
from logistic_regression import LogisticRegression
from random_forest import RandomForest


def accuracy_score(y_true, y_predict):
    return np.sum(np.array(y_true) == np.array(y_predict))*1./len(y_true)


def plot_data(X, y, name=""):
    x1 = X[:, 0]
    x2 = X[:, 1]
    print(x1.shape, x2.shape, y.shape)
    plt.clf()
    plt.savefig("pic.png")
    plt.plot(x1[y == 1], x2[y == 1], '.r')
    plt.plot(x1[y == 0], x2[y == 0], '.b')
    plt.show()
    plt.savefig("pic" + name + ".png")


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
    filename = 'data/SPECTF.dat'
    data = np.loadtxt(filename, delimiter=',')
    X = data[:, 1:]
    y = np.array(data[:, 0])

    n, d = X.shape
    print(X.shape, y.shape, n, d)

    dt = DecisionTree(50)
    dt.fit(X, y)
    all_accuracies = {
        "decision tree":[],
        "logistic regression":[],
        "random forest":[],
    }
    for trial in range(20):
        print("TRIAL: " + str(trial))
        perm = np.random.permutation(len(y))
        X = X[perm]
        y = y[perm]

        X_train = X[0:100, :]  # train on first 100 instances
        X_test = X[100:, :]
        y_train = y[0:100]  # test on remaining instances
        y_test = y[100:]

        classifier = DecisionTree(100)
        classifier.fit(X_train, y_train)
        y_predicted = classifier.predict(X_test)
        all_accuracies["decision tree"].append(accuracy_score(y_test, y_predicted))

        classifier = LogisticRegression()
        classifier.train(X_train, y_train)
        y_predicted = classifier.predict(X_test)
        all_accuracies["logistic regression"].append(accuracy_score(y_test, y_predicted))

        classifier = RandomForest(10,10,0.4)
        classifier.fit(X_train, y_train)
        y_predicted, conf = classifier.predict(X_test)
        all_accuracies["random forest"].append(accuracy_score(y_test, y_predicted))

    # print(all_accuracies)

    # compute the training accuracy of the model
    mean_decision_tree_accuracy = np.mean(all_accuracies["decision tree"])
    stddev_decision_tree_accuracy = np.std(all_accuracies["decision tree"])

    mean_logistic_regression_accuracy = np.mean(all_accuracies["logistic regression"])
    stddev_logistic_regression_accuracy = np.std(all_accuracies["logistic regression"])

    mean_random_forest_accuracy = np.mean(all_accuracies["random forest"])
    stddev_andom_forest_accuracy = np.std(all_accuracies["random forest"])

    # make certain that the return value matches the API specification
    stats = np.zeros((3, 2))
    stats[0, 0] = mean_decision_tree_accuracy
    stats[0, 1] = stddev_decision_tree_accuracy
    stats[1, 0] = mean_random_forest_accuracy
    stats[1, 1] = stddev_andom_forest_accuracy
    stats[2, 0] = mean_logistic_regression_accuracy
    stats[2, 1] = stddev_logistic_regression_accuracy
    return stats


# Do not modify from HERE...
if __name__ == "__main__":
    stats = evaluate_performance()
    print("Decision Tree Accuracy = ", stats[0, 0], " (", stats[0, 1], ")")
    print("Random Forest Accuracy = ", stats[1, 0], " (", stats[1, 1], ")")
    # stats = evaluate_performance()
    print( "Logistic Reg. Accuracy = ", stats[2, 0], " (", stats[2, 1], ")")
# ...to HERE.
