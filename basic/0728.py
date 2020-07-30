import numpy as np
'''
from activate import sigmoid_fx as Fx
from activate import sigmoid_df as DFx
'''
from activate import relu_fx as Fx
from activate import relu_df as DFx


batch = 500
learning_rate = 0.01

def fx(x,w,b):
    y = np.dot(x,w) + b
    res = Fx(y)
    return res

def loss(delta):
    return delta**2/2

def grad(x,w,b,y):
    delta = (fx(x,w,b) - y)
    n_sample = x.shape[0]
    delta /= n_sample
    df = DFx(fx(x,w,b))
    dv = np.column_stack((x,np.ones(n_sample)))
    return np.dot(delta*df,dv)

def main():
    x = np.array(
        [[1,2],
        [2,3],
        [3,4]])
    y = np.array([5.5,8.7,11.9])
    n_sample = x.shape[0]
    n_feature = x.shape[1]
    theta = np.array([1,1,-0.5])
    #theta = np.random.rand(n_feature+1)
    w = theta[0:n_feature]
    b = theta[n_feature]

    for i in range(1,batch):
        delta = fx(x,w,b) - y
        Loss = sum(loss(delta)) / n_sample
        if Loss < 0.01:
            print(w,b)
            return
        else:
            g = grad(x,w,b,y)
            print(Loss,g)
            delta_g = g * learning_rate
            w = w - delta_g[0:n_sample-2]
            b = b - delta_g[n_sample-1]        

main()