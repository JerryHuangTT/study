import numpy as np
from sklearn import preprocessing
rng = np.random

X = np.array([1.003,0.122,0.355,0.71,0.93,4.168,9.779,3.182,2.59,2.167,
              1.042,1.12,0.313,2.997,4.654,10.27,3.1])
X = preprocessing.scale(X) #正则化
Y = np.sin(X) #+ rng.normal(0, 0.5, None) # 0-1高斯白噪声
 #+  np.random.normal(0, 0.5, None)`  


# Parameters.
learning_rate = 0.01
training_steps = 1000
display_step = 100    

import tensorflow as tf
# Weight and Bias, initialized randomly.
W = tf.Variable(rng.randn(), name="weight")
b = tf.Variable(rng.randn(), name="bias")

# Linear regression (Wx + b).
def linear_regression(x):
    return W * x + b

# Mean square error.
def mean_square(y_pred, y_true):
    return tf.reduce_mean(tf.square(y_pred - y_true))

# Stochastic Gradient Descent Optimizer.
optimizer = tf.optimizers.SGD(learning_rate)

# Optimization process. 
def run_optimization():
    # Wrap computation inside a GradientTape for automatic differentiation.
    with tf.GradientTape() as g:
        pred = linear_regression(X)
        loss = mean_square(pred, Y)

    # Compute gradients.
    gradients = g.gradient(loss, [W, b])
    
    # Update W and b following gradients.
    optimizer.apply_gradients(zip(gradients, [W, b]))

# Run training for the given number of steps.
for step in range(1, training_steps + 1):
    # Run the optimization to update W and b values.
    run_optimization()
    
    if step % display_step == 0:
        pred = linear_regression(X)
        loss = mean_square(pred, Y)
        print("step: %i, loss: %f, W: %f, b: %f" % (step, loss, W.numpy(), b.numpy()))    