import numpy as np

def sigmoid_fx(x):
    return 1/(1+np.exp(-x))

def sigmoid_df(x):
    return sigmoid_fx(x)*(1-sigmoid_fx(x))

def relu_fx(x):
    return np.maximum(0,x)

def relu_df(x):
    dZ = np.array(x, copy=True)
    dZ[x <= 0] = 0
    dZ[x > 0] = 1
    assert(dZ.shape == x.shape) #确保维度相同
    return dZ