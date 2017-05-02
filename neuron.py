import numpy as np
import random


def sigmoid(s):
    return 1. / (1. + np.exp(-s))


def sigmoid_derivative(s):
    sigmoid_value = sigmoid(s)
    return sigmoid_value * (1. - sigmoid_value)


class Neuron(object):
    def __init__(self,
                 n_inputs,
                 weights=None,
                 transfer_function=sigmoid,
                 transfer_function_derivative=sigmoid_derivative):

        self.transfer_function = transfer_function
        if weights is None:
            self.weights = [1e-5 * random.random()
                            for _ in range(n_inputs + 1)]
        else:
            assert n_inputs == len(weights) - 1
            self.weights = weights
        self.derivative_function = transfer_function_derivative

        # Values for the last feed-forward
        self.weighted_sum = None
        self.output = None
        self.inputs = None
        # Values for the last feed-backward
        self.delta = None

    def forward_propagate(self, inputs):
        weighted_sum = self.weights[0]
        # print(range(1, len(self.weights)))
        for i in range(1, len(self.weights)):
            weighted_sum += self.weights[i] * inputs[i - 1]
        self.weighted_sum = weighted_sum
        self.output = self.transfer_function(weighted_sum)
        self.inputs = inputs
        return self.output

    def feed_backwards(self, error):
        self.delta = self.derivative_function(self.weighted_sum) * error
        errors = []
        for i in range(1, len(self.weights)):
            errors.append(self.delta * self.weights[i])
        return errors

    def update_weights(self, learning_rate):
        self.weights[0] -= learning_rate * self.delta
        for i in range(1, len(self.weights)):
            self.weights[i] -= learning_rate * self.delta * self.inputs[i - 1]
