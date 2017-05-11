import numpy as np
import theano
import theano.tensor as T
import pickle

from mnist import load_dataset

__file_path__ = './params_54216786'

X_train, y_train, X_val, y_val, X_test, y_test = load_dataset()

# hot_points = np.std(X_train[:,0,...],axis=0)
H = np.arange(1, 27)
W = np.arange(3, 25)

X_test = X_test[..., H, :][..., W]
X_train = X_train[..., H, :][..., W]
X_val = X_val[..., H, :][..., W]

input_X = T.tensor4('X')
input_shape = [None]
input_shape.extend(X_train.shape[1:])
# print(input_shape)
target_y = T.vector("target Y integer",dtype='int32')


################################
import lasagne
from lasagne.layers import *

layer = InputLayer(shape = input_shape,input_var=input_X)


layer = Conv2DLayer(layer, num_filters=34, filter_size=(5, 5), pad='same', nonlinearity=lasagne.nonlinearities.rectify)


layer = MaxPool2DLayer(layer, (2,2))

layer = Conv2DLayer(layer, num_filters=31, filter_size=(5, 5), pad='same', nonlinearity=lasagne.nonlinearities.rectify)

layer = MaxPool2DLayer(layer, (2,2))

layer = DropoutLayer(layer, p=0.5)

layer = DenseLayer(layer, num_units=911, nonlinearity=lasagne.nonlinearities.rectify)

layer = DropoutLayer(layer, p=0.3)

layer = DenseLayer(layer,num_units = 10,nonlinearity=lasagne.nonlinearities.softmax)

##############################################
y_test_predicted = lasagne.layers.get_output(layer, deterministic=True)
parameters = lasagne.layers.get_all_params(layer)
accuracy = lasagne.objectives.categorical_accuracy(y_test_predicted,target_y).mean()
accuracy_fun = theano.function([input_X,target_y],accuracy)


with open(__file_path__, 'rb') as input_stream:
    history, saved_parameters, epoch = pickle.load(input_stream)
    for saved_parameter, parameter in zip(saved_parameters, parameters):
        parameter.set_value(saved_parameter)
    last_saved_epoch = epoch


batch_size = 300  # number of samples processed at each function call

def iterate_minibatches(inputs, targets, batchsize):
    assert len(inputs) == len(targets)
    indices = np.arange(len(inputs))
    np.random.shuffle(indices)
    for start_idx in range(0, len(inputs) - batchsize + 1, batchsize):
        excerpt = indices[start_idx:start_idx + batchsize]
        yield inputs[excerpt], targets[excerpt]


def accuracy(X, y):
    acc = 0
    batches = 0
    for batch in iterate_minibatches(X, y, 500):
        inputs, targets = batch
        acc = acc + accuracy_fun(inputs, targets)
        batches += 1
    return acc*1. / batches


print('Epoch: {}'.format(last_saved_epoch))
print("Training set accuracy:\t\t{:.2f} %".format(accuracy(X_train, y_train) * 100))
print("Validation set accuracy:\t{:.2f} %".format(accuracy(X_val, y_val) * 100))
print("Test set accuracy:\t\t{:.2f} %".format(accuracy(X_test, y_test) * 100))
