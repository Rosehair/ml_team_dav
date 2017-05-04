import numpy as np
import math as math


def sigmoid(s):
    return 1 / (1 + np.exp(-s))


def normalized_gradient(X, Y, beta):

    x_mean = np.array([np.mean(X.T[i]) for i in range(X.shape[1])])

    grad = sum(-(1 - sigmoid(beta.T.dot(X[i]) * Y[i])) * X[i]*Y[i] for i in range(X.shape[0]))

    grad = np.array([grad[i] / (X.shape[0] * x_mean[i]) for i in range(x_mean.shape[0])])

    # print(grad)

    return grad


def gradient_descent(X, Y, epsilon=1e-6, l=1, step_size=1e-4, max_steps=1000):

    beta = np.zeros(X.shape[1])

    beta_last = beta

    for s in range(max_steps):

        grad = normalized_gradient(X, Y, beta)

        if s !=0:

            beta_last = beta



        # beta = beta - step_size * grad

        beta1 = beta[1:] - step_size*(grad[1:] + l * np.array(beta[1:]))

        beta0 = beta[0] - step_size*(grad[0])

        beta = np.concatenate((np.array([beta0]), beta1))



        # print(math.fabs(np.linalg.norm(beta_last - beta)/np.linalg.norm(beta)))
        # print(np.linalg.norm(beta_last))
        if math.fabs(np.linalg.norm(beta_last - beta)/np.linalg.norm(beta)) < epsilon:

            # print(s)

            break

    return beta



# def gradient_descent(X, Y, epsilon=1e-6, l=1, step_size=1e-4, max_steps=1000):
#     """
#     Implement gradient descent using full value of the gradient.
#     :param X: data matrix (2 dimensional np.array)
#     :param Y: response variables (1 dimensional np.array)
#     :param l: regularization parameter lambda
#     :param epsilon: approximation strength
#     :param max_steps: maximum number of iterations before algorithm will
#         terminate.
#     :return: value of beta (1 dimensional np.array)
#     """
#     Y = np.reshape(Y, (1, np.size(Y))).flatten()
#     beta = np.zeros(X.shape[1])
#     for s in range(max_steps):
#         if s % 1000 == 0:
#             print(s, beta)
#
#         print(np.shape(X))
#         print(np.shape(beta))
#         print(np.shape(X * beta))
#         print(np.shape(Y))
#         print(np.shape(sigmoid(Y.dot(X * beta))))
#
#         beta = X.T * Y.dot(sigmoid(Y.dot(X * beta)))
#         print(beta)
#     return beta
