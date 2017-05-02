from neuron import Neuron
import numpy as np


class NeuralNetwork(object):

    def __init__(self, n_features, neurons_per_layer):
        layers = []
        for layer in range(len(neurons_per_layer)):
            _layer = []
            if layer is 0: n_imput = n_features
            else: n_imput = neurons_per_layer[layer-1]
            for neuron in range(neurons_per_layer[layer]):
                _layer.append(Neuron(n_imput))
            layers.append(_layer)
            # print(_layer,layers)

        self.layers = layers
        self.output = None

    def forward_propagate(self, features):
        new_features = []
        for index, layer in enumerate(self.layers):
            if index is not 0:
                features = new_features
                new_features = []

            for neuron in layer:
                new_features.append(neuron.forward_propagate(features))
            features = new_features


        self.output = features
        return self.output

    def backward_propagate(self, correct_output_vector):
        out_error = [out - true for true, out in zip(correct_output_vector, self.output)]

        if np.argmax(correct_output_vector) == np.argmax(self.output):
            self.answer = True
        else:
            self.answer = False

        for index in range(len(self.layers) - 1, -1, -1):
            error = np.zeros(len(self.layers[index][0].inputs))

            for i, neuron in enumerate(self.layers[index]):
                error += np.array(neuron.feed_backwards(out_error[i]))
            out_error = error

    def update_weights(self, learning_rate):
        for layer in self.layers:
            for neuron in layer:
                neuron.update_weights(learning_rate)

    def train(self, X, Y, learning_rate=1e-7, max_iter=1):
        for j, x in enumerate(X):
            self.forward_propagate(x)
            self.backward_propagate(Y[j])
            self.update_weights(learning_rate)
            print(j, self.answer)