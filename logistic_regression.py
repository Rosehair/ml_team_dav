"""logistic regression implementation by Vardges Mambreyan"""
import numpy as np
from scipy.special import expit


def sigmoid(value):
    """sigmoid function"""
    return expit(value)


def normalized_gradient(data, labels, beta):
    """calculates normalized gradient"""
    grad = sum(-(1 - sigmoid(beta.T.dot(data[i]) * labels[i])) * data[i] * labels[i]
               for i in range(data.shape[0]))
    grad = np.array([grad[i] / (data.shape[0]) for i in range(data.shape[1])])
    return grad


def gradient_descent(data, labels, l_reg=1, step_size=0.0001, max_steps=1000):
    """
    gradient descent with step size,
    it will end when looping max_steps times
    """

    for step in range(labels.shape[0]):
        if labels[step] == 0:
            labels[step] = -1
    beta = np.zeros(data.shape[1])

    for _ in range(max_steps):
        grad = normalized_gradient(data, labels, beta)

        beta1 = beta[1:] - step_size*(grad[1:] + l_reg * np.array(beta[1:]))
        beta0 = beta[0] - step_size*(grad[0])
        beta = np.concatenate((np.array([beta0]), beta1))

    return beta


def gradient_predict(data, beta):
    """predicts labels for the data"""
    labels = []
    for step in range(data.shape[0]):
        if beta.dot(data[step]) > 0:
            labels.append(1)
        else: labels.append(-1)
    return np.array(labels)



