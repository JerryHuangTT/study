import numpy as np

batch = 50
learning_rate = 0.01

def fx(x,w,b):
    return np.dot(x,w) + b

def loss(delta):
    return delta**2/2

def grad(delta,x):
    n_sample = x.shape[0]
    delta /= n_sample
    t = np.column_stack((x,np.ones(n_sample)))
    theta = np.dot(delta,t)
    return theta

def main():
    x = np.array(
        [[1,2],
        [2,3],
        [3,4]])
    y = np.array([5.5,8.7,11.9])
    n_sample = x.shape[0]
    n_feature = x.shape[1]
    theta = np.random.rand(n_feature+1)
    w = theta[0:n_feature]
    b = theta[n_feature]

    for i in range(1,batch):
        delta = fx(x,w,b) - y
        Loss = sum(loss(delta)) / n_sample
        if Loss < 0.01:
            print(w,b)
            return
        else:
            g = grad(delta,x)
            print(Loss,g)
            delta_g = g * learning_rate
            w = w - delta_g[0:n_sample-2]
            b = b - delta_g[n_sample-1]        

main()