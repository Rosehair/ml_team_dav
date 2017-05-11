import numpy as np
import theano
import theano.tensor as T
import pickle

from mnist import load_dataset
__code__ = str(54216787)

__file_path__ = './params_' + __code__

X_train,y_train,X_val,y_val,X_test,y_test = load_dataset()

# hot_points = np.std(X_train[:,0,...],axis=0)

H = np.arange(1, 27)
W = np.arange(3, 25)

X_test = X_test[..., H, :][..., W]
X_train = X_train[..., H, :][..., W]
X_val = X_val[..., H, :][..., W]

print('Training', X_train.shape, y_train.shape)
print('Validation', X_val.shape, y_val.shape)
print('Test', X_test.shape, y_test.shape)

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

layer = DropoutLayer(layer, p=0.68)

layer = DenseLayer(layer, num_units=911, nonlinearity=lasagne.nonlinearities.rectify)

layer = DropoutLayer(layer, p=0.41)

layer = DenseLayer(layer,num_units = 10,nonlinearity=lasagne.nonlinearities.softmax)
##############################################
y_predicted = lasagne.layers.get_output(layer)
y_test_predicted = lasagne.layers.get_output(layer, deterministic=True)
parameters = lasagne.layers.get_all_params(layer)
loss = lasagne.objectives.categorical_crossentropy(y_predicted,target_y).mean()
accuracy = lasagne.objectives.categorical_accuracy(y_test_predicted,target_y).mean()
updates_sgd = lasagne.updates.nesterov_momentum(loss, parameters, learning_rate=0.09,momentum=0.82)
train_fun = theano.function([input_X,target_y],[loss,accuracy],updates= updates_sgd)
accuracy_fun = theano.function([input_X,target_y],accuracy)

def iterate_minibatches(inputs, targets, batchsize):
    assert len(inputs) == len(targets)
    indices = np.arange(len(inputs))
    np.random.shuffle(indices)
    for start_idx in range(0, len(inputs) - batchsize + 1, batchsize):
        excerpt = indices[start_idx:start_idx + batchsize]
        yield inputs[excerpt], targets[excerpt]


loss_history = []
train_acc_history = []
val_acc_history = []
epoch = 0
last_saved_epoch = 0


def dump():
    saved_parameters = []
    for parameter in parameters:
        saved_parameters.append(parameter.get_value())
    save = ((loss_history,train_acc_history,val_acc_history),
            saved_parameters,
            epoch)
    with open(__file_path__, 'wb') as output_stream:
        pickle.dump(save, output_stream, -1)


from pathlib import Path
if Path(__file_path__).is_file():
    with open(__file_path__, 'rb') as input_stream:
        history, saved_parameters, epoch = pickle.load(input_stream)
        for saved_parameter, parameter in zip(saved_parameters, parameters):
            parameter.set_value(saved_parameter)
        last_saved_epoch = epoch
        loss_history = history[0]
        train_acc_history = history[1]
        val_acc_history = history[2]


import time

batch_size = 100  # number of samples processed at each function call



print('Start Training')
stdout = open('./stdout_' + __code__ + '.txt', 'w')
while True:
    loss_history = loss_history[-1000:]
    val_acc_history = val_acc_history[-1000:]
    train_acc_history = train_acc_history[-1000:]
    epoch = epoch + 1
    train_err = 0
    train_acc = 0
    train_batches = 0
    start_time = time.time()
    for batch in iterate_minibatches(X_train, y_train, batch_size):
        inputs, targets = batch
        train_err_batch, train_acc_batch = train_fun(inputs, targets)
        train_err += train_err_batch
        train_acc += train_acc_batch
        train_batches += 1

    # And a full pass over the validation data:
    val_acc = 0
    val_batches = 0
    for batch in iterate_minibatches(X_val, y_val, batch_size):
        inputs, targets = batch
        val_acc += accuracy_fun(inputs, targets)
        val_batches += 1

    loss = train_err / train_batches
    val_acc = val_acc / val_batches * 100
    train_acc = train_acc / train_batches * 100
    loss_history.append(loss)
    train_acc_history.append(train_acc)
    val_acc_history.append(val_acc)

    print("Epoch {} took {:.3f}s (last saved epoch {})".format(epoch,  time.time() - start_time, last_saved_epoch))
    print("  training loss:\t\t{:.6f}".format(loss))
    print("  train accuracy:\t{:.2f} %".format(train_acc))
    print("  validation accuracy:\t{:.2f} %".format(val_acc))
    stdout.write("Epoch {} took {:.3f}s (last saved epoch {}) \n".format(epoch,  time.time() - start_time, last_saved_epoch))
    stdout.write("  training loss:\t\t{:.6f} \n".format(loss))
    stdout.write("  train accuracy:\t{:.2f} % \n".format(train_acc))
    stdout.write("  validation accuracy:\t{:.2f} % \n".format(val_acc))
    if epoch % 3 == 0:
        dump()
        print('Saved!!!')
        stdout.write('Saved!!!\n')
    stdout.flush()

