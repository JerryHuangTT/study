import numpy as np

def sigmoid_fx(x):
    return 1/(1+np.exp(-x))

def relu_fx(x):
    return np.maximum(0,x)

def sigmoid_df(x):
    return sigmoid_fx(x)*(1-sigmoid_fx(x))

def relu_df(X):
    res = []
    for x in X:
        if x < 0:
            res.append(0)
        else:
            res.append(1)
    return res        