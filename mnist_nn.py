import random
from neural_network import NeuralNetwork
import gzip
import struct
import argparse
import matplotlib.pyplot as plt
import numpy as np


def test(network, num_data=10000):
    errors = 0
    i=0
    for img, true_label in zip(test_data[:num_data], test_labels[:num_data]):
        i+=1
        out_v = network.forward_propagate(img.reshape(-1))
        errors += 0 if np.argmax(out_v) == true_label else 1
        print(i,'{:.2f}% error rate'.format(100. * errors / i))
    print('{:.2f}% error rate'.format(100. * errors / len(test_data)))


def show_10_neurons(network):
    _10_neurons(network, show=True)


def save_10_neurons(network, path):
    _10_neurons(network, savefig=path)


def _10_neurons(network, show=False, savefig=None):
    plt.clf()
    plot_rows, plot_columns = 2, 5
    f, axarr = plt.subplots(plot_rows, plot_columns)
    for i in range(plot_rows):
        for j in range(plot_columns):
            n = network.layers[0][plot_columns * i + j]
            weight_img = np.reshape(n.weights[1:], (rows, columns))
            axarr[i, j].imshow(weight_img, cmap='Greys')
    if savefig:
        plt.savefig(savefig)
    if show:
        plt.show()


def parse_args(*argument_array):
    parser = argparse.ArgumentParser()
    parser.add_argument('--mnist-train-data',
                        default='train-images-idx3-ubyte.gz',  # noqa
                        help='Path to train-images-idx3-ubyte.gz file '
                        'downloaded from http://yann.lecun.com/exdb/mnist/')
    parser.add_argument('--mnist-train-labels',
                        default='train-labels-idx1-ubyte.gz',  # noqa
                        help='Path to train-labels-idx1-ubyte.gz file '
                        'downloaded from http://yann.lecun.com/exdb/mnist/')
    parser.add_argument('--mnist-test-data',
                        default='t10k-images-idx3-ubyte.gz',
                        help='Path to t10k-images-idx3-ubyte.gz file '
                             'downloaded from http://yann.lecun.com/exdb/mnist/')  # noqa
    parser.add_argument('--mnist-test-labels',
                        default='t10k-labels-idx1-ubyte.gz',
                        help='Path to t10k-labels-idx1-ubyte.gz file '
                             'downloaded from http://yann.lecun.com/exdb/mnist/')
    parser.add_argument('--positive-label', type=int, choices=list(range(10)),
                        default=9)
    parser.add_argument('--negative-label', type=int, choices=list(range(10)),
                        default=4)
    parser.add_argument('--limit-to', nargs='*',
                        help='Limit to the specified files.')
    args = parser.parse_args(*argument_array)
    return args


if __name__ == '__main__':
    args = parse_args()

    # Read labels file into labels
    with gzip.open(args.mnist_train_labels, 'rb') as in_gzip:
        magic, num = struct.unpack('>II', in_gzip.read(8))
        all_labels = struct.unpack('>60000B', in_gzip.read(60000))

    # Read data file into numpy matrices
    with gzip.open(args.mnist_train_data, 'rb') as in_gzip:
        magic, num, rows, columns = struct.unpack('>IIII', in_gzip.read(16))
        all_data = [np.reshape(struct.unpack('>{}B'.format(rows * columns),
                                             in_gzip.read(rows * columns)),
                               (rows, columns))
                    for _ in range(60000)]

    # Read labels file into labels
    with gzip.open(args.mnist_test_labels, 'rb') as in_gzip:
        magic, num = struct.unpack('>II', in_gzip.read(8))
        test_labels = struct.unpack('>10000B', in_gzip.read(10000))

    # Read data file into numpy matrices
    with gzip.open(args.mnist_test_data, 'rb') as in_gzip:
        magic, num, rows, columns = struct.unpack('>IIII', in_gzip.read(16))
        test_data = [np.reshape(struct.unpack('>{}B'.format(rows * columns),
                                              in_gzip.read(rows * columns)),
                                (rows, columns))
                     for _ in range(10000)]

    vector_data = [img.reshape(-1) for img in all_data]

    vector_labels = [np.zeros(10) for _ in all_labels]
    for v, y in zip(vector_labels, all_labels):
        v[y] = 1
    #
    one_layer_network = NeuralNetwork(784,[10, 5, 10])
    # print(vector_data[:1])
    # print(vector_labels[:1])
    # print(len(vector_data))
    # N = 100



    training_set_size = 60000
    one_layer_network.train(vector_data[:training_set_size],
        vector_labels[0:training_set_size], max_iter=1)

    # print(all_labels[-1], one_layer_network.forward_propagate(vector_data[-1]))

    test(one_layer_network)
    # Plot 10 neuron weights.
    # save_10_neurons(one_layer_network,path="pic")

