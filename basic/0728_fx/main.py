import numpy as np
'''
from activate import sigmoid_fx as Fx
from activate import sigmoid_df as DFx
'''
from activate import relu_fx as Fx
from activate import relu_df as DFx

X = np.array(
    [[1,2],
    [2,3],
    [3,4],
    [4,5],
    [5,6],
    [6,7]])
Y = np.array([5,8,11,14,17,20])
batch = 5000
learning_rate = 0.01

def fx(x,w,b):
    y = np.dot(x,w) + b
    return Fx(y)

def loss(delta):
    return delta**2/2

def grad(x,w,b,delta):
    n_sample = x.shape[0]
    df = DFx(fx(x,w,b))
    dv = np.column_stack((x,np.ones(n_sample)))
    return np.dot(delta*df,dv) / n_sample

def run_optimization(x,y):
    n_feature = x.shape[1]
    #theta = np.array([1,1,-0.5])
    theta = np.random.rand(n_feature+1)
    w = theta[0:n_feature]
    b = theta[n_feature]
    for i in range(1,batch):
        delta = fx(x,w,b) - y
        Loss = sum(loss(delta)) / x.shape[0]
        if Loss < 0.00001:
            print(i)
            return [w,b]
        else:
            g = grad(x,w,b,delta)
            #print(i,Loss,g)
            delta_g = -g * learning_rate
            w = w + delta_g[0:n_feature]
            b = b + delta_g[n_feature]   
    return [w,b]             

w,b = run_optimization(X,Y)
y_pred = fx(X,w,b)
print(y_pred-Y)