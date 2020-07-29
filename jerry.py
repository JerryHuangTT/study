import numpy as np
import math

X1 = np.array([1,2,3])
X2 = np.array([2,3,4])
Y = np.array([5.5,8.7,11.9])

def fx(x1,x2,w1,w2,b):
    return x1*w1 + x2*w2 + b

def loss(x1,x2,y,w1,w2,b):
    t = fx(x1,x2,w1,w2,b)-y  
    return 1/2*math.pow(t,2)

def grad(w1,w2,b):
    n = Y.shape[0]
    r1 = 0
    r2 = 0
    r3 = 0
    for i in range(0,n):
        t = fx(X1[i],
        X2[i],
        w1,
        w2,
        b)- Y[i]
        r1 += t * X1[i] / n
        r2 += t * X2[i] / n
        r3 += 1 * t / n
    return [r1,r2,r3]

def run_optimization(w1,w2,b):
    n = Y.shape[0]
    l = 0
    for i in range(0,n):
        l += loss(X1[i],
        X2[i],
        Y[i],
        w1,
        w2,
        b)
    return l / n

def main():
    w1 = np.random.randn()
    w2 = np.random.randn()
    b = np.random.randn()
    batch = 50000
    learning_rate = 0.01
    for i in range(1,batch):
        l = run_optimization(w1,w2,b)
        if l < 0.01:
            print([i,w1,w2,b,l])
            break
        g = grad(w1,w2,b)
        w1 -= learning_rate * g[0]
        w2 -= learning_rate * g[1]
        b  -= learning_rate * g[2]

main()