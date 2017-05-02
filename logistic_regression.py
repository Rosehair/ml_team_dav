import numpy as np
from scipy.special import expit
import math as math


def sigmoid(s):
    return expit(s)


def normalized_gradient(X, Y, beta):

    grad = sum(-(1 - sigmoid(beta.T.dot(X[i]) * Y[i])) * X[i]*Y[i] for i in range(X.shape[0]))
    grad = np.array([grad[i] / (X.shape[0]) for i in range(X.shape[1])])
    return grad


def gradient_descent(X, Y, epsilon=1e-6, l=1, step_size=0.0001, max_steps=1000):

    for s in range(Y.shape[0]):
        if Y[s] == 0: Y[s] = -1

    beta = np.zeros(X.shape[1])

    for s in range(max_steps):
        grad = normalized_gradient(X, Y, beta)

        beta1 = beta[1:] - step_size*(grad[1:] + l * np.array(beta[1:]))
        beta0 = beta[0] - step_size*(grad[0])
        beta = np.concatenate((np.array([beta0]), beta1))

    return beta


def gradient_predict(X, beta):
    Y =[]
    for s in range(X.shape[0]):
        if beta.dot(X[s]) > 0: Y.append(1)
        else: Y.append(-1)
    return np.array(Y)



