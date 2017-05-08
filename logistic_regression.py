import numpy as np


class LogisticRegression(object):
    def __init__(self):
        self.beta = None

    @staticmethod
    def sigmoid(s):
        return 1 / (1 + np.exp(np.negative(s)))

    @staticmethod
    def sigmoid_array(s):
        sig = np.zeros(s.shape)
        sig[s >= 0] = 1 / (1 + np.exp(-s[s >= 0]))
        sig[s < 0] = np.exp(s[s < 0]) / (1 + np.exp(s[s < 0]))
        return sig

    @staticmethod
    def normalized_gradient(X, y, beta, l):
        y = np.array(y)
        gradient = np.zeros(len(beta))
        gradient = (X.T.dot(-1 * y * LogisticRegression.sigmoid_array(-1 * y * (X.dot(beta)))) + l * beta) / len(X)
        return gradient

    @staticmethod
    def gradient_descent(X, y, beta_start, l=1, step_size=0.001,
                         max_epoch=100, batch_size=100):
        y = np.array(y)
        beta_norm = np.zeros(X.shape[1])
        a = np.mean(X[:, 1:], axis=0)
        m = np.max(np.abs(X[:, 1:] - a), axis=0) / 2 + 1
        b = np.std(X[:, 1:], axis=0)
        b[b < m] = m[b < m]
        beta_norm[1:] = beta_start[1:] * b
        beta_norm[0] = beta_start[0] + a.dot(beta_start[1:])
        X_norm = np.column_stack((X[:, 0], (X[:, 1:] - a) / b))
        y_norm = y
        l_norm = np.hstack((0, l / (b ** 2)))
        for epoch in range(max_epoch):
            perm = np.random.permutation(len(X_norm))
            X_norm = X_norm[perm]
            y_norm = y_norm[perm]
            for start in range(0, len(X), batch_size):
                end = start + batch_size
                X_batch = X_norm[start:end]
                y_batch = y_norm[start:end]
                grad = LogisticRegression.normalized_gradient(X_batch, y_batch, beta_norm, l_norm)
                delta = step_size * grad
                beta_norm = beta_norm - delta

        beta = np.hstack(((beta_norm[0] - a.dot(beta_norm[1:] / b)), beta_norm[1:] / b))
        return beta

    def predict(self, X):
        X = np.column_stack((np.ones(len(X)),X))
        return np.array([1 if a > 0.5 else 0 for a in LogisticRegression.sigmoid_array(X.dot(self.beta))])

    def fit(self, X, y, l=1, step_size=0.001, max_epoch=20):
        X = np.column_stack((np.ones(len(X)),X))
        self.beta = np.zeros(X.shape[1])
        self.beta = LogisticRegression.gradient_descent(X, y, self.beta, l, step_size=step_size, max_epoch=max_epoch,
                                                        batch_size=5)
