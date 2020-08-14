from tensorflow.keras.datasets import mnist
import tensorflow as tf
from tensorflow.keras import Model, layers

import pandas as pd
import numpy as np
from imblearn.over_sampling import SMOTE

num_classes = 0
def load_data():
    global num_classes
    data = pd.read_excel('tf2\\classification\\0812\\pump.xlsx')
    num_classes = data['type'].value_counts().shape[0]
    i = 0
    for l in data['type'].value_counts().index:
        data.loc[data['type'] == l] = i
        i += 1
    print(data['type'].value_counts())    
    train_data = data.sample(frac=0.7,random_state=None)
    test_data = data.drop(train_data.index)

    n = train_data.shape[1]-1
    x,y = train_data.iloc[:,0:n], train_data.iloc[:,n]
    smo = SMOTE(random_state=42)
    ex_x,ex_y = smo.fit_sample(x,y)
    ex_x.insert(ex_x.shape[1], 'type', ex_y)
    train_data = ex_x
    print(train_data['type'].value_counts())
    print(test_data['type'].value_counts())
    return train_data.values,test_data.values

def parse_data():
    train_data,test_data = load_data()
    n = train_data.shape[1]-1
    x_train = train_data[:,0:n].astype('float64')
    y_train = train_data[:,n]
    n = test_data.shape[1]-1
    x_test = test_data[:,0:n].astype('float64')
    y_test = test_data[:,n]
    return (x_train, y_train), (x_test, y_test)

(x_train, y_train), (x_test, y_test) = parse_data()
n_hidden_1 = 64 # 1st layer number of neurons.
n_hidden_2 = 64  # 2nd layer number of neurons.
n_hidden_3 = 32 # 2nd layer number of neurons.
#num_classes = x_train.shape[1] * x_train.shape[2]
learning_rate = 0.001
train_data = tf.data.Dataset.from_tensor_slices((x_train, y_train))
train_data = train_data.repeat().batch(512).prefetch(1)
#train_data = train_data.repeat().shuffle(5000).batch(256).prefetch(1)

class NeuralNet(Model):
    def __init__(self):
        super(NeuralNet, self).__init__()
        self.fc1 = layers.Dense(n_hidden_1, activation=tf.nn.relu)
        self.fc2 = layers.Dense(n_hidden_2, activation=tf.nn.relu)
        self.fc3 = layers.Dense(n_hidden_3, activation=tf.nn.relu)
        self.out = layers.Dense(num_classes)

    def call(self, x, is_training=False):
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.fc3(x)
        x = self.out(x)
        if not is_training:
            x = tf.nn.softmax(x)
        return x

neural_net = NeuralNet()

def cross_entropy_loss(x, y):
    # Convert labels to int 64 for tf cross-entropy function.
    y = tf.cast(y, tf.int64)
    # Apply softmax to logits and compute cross-entropy.
    loss = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=x)
    # Average loss across the batch.
    return tf.reduce_mean(loss)

def accuracy(y_pred, y_true):
    # Predicted class is the index of highest score in prediction vector (i.e. argmax).
    correct_prediction = tf.equal(tf.argmax(y_pred, 1), tf.cast(y_true, tf.int64))
    return tf.reduce_mean(tf.cast(correct_prediction, tf.float32), axis=-1)

optimizer = tf.optimizers.SGD(learning_rate)

for i, (x, y) in enumerate(train_data.take(20000), 1):
    with tf.GradientTape() as g:
        pred = neural_net(x, is_training=True)
        loss = cross_entropy_loss(pred, y)
    trainable_variables = neural_net.trainable_variables
    gradients = g.gradient(loss, trainable_variables)
    optimizer.apply_gradients(zip(gradients, trainable_variables))

    if i % 500 == 0:
        pred = neural_net(x, is_training=True)
        loss = cross_entropy_loss(pred, y)
        acc = accuracy(pred, y)
        print("step: %i, loss: %f, accuracy: %f" % (i, loss, acc))

def pred(x,y):
    pred = neural_net(x)
    print("validation accuracy: %f" % accuracy(pred, y))

pred(x_test, y_test)