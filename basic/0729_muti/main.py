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

X = np.array([[3.3,4.4,5.5,6.71,6.93,4.168,9.779,6.182,7.59,2.167,
                         7.042,10.791,5.313,7.997,5.654,9.27,3.1]])
Y = np.array([1.7,2.76,2.09,3.19,1.694,1.573,3.366,2.596,2.53,1.221,
                         2.827,3.465,1.65,2.904,2.42,2.94,1.3])

batch = 5000
learning_rate = 0.01
n_sample = X.shape[0]
n_feature = 1#X.shape[1]

def fx(x,w,b):
    y = np.dot(x,w) + b
    return Fx(y)

def loss(delta):
    return delta**2/2

def grad(x,w,b,loss):
    n_sample = x.shape[0]
    df = DFx(fx(x,w,b))
    dv = np.column_stack((x,np.ones(n_sample)))
    g = np.dot(loss*df,dv)
    return g / n_sample

def run_optimization(x,y):
    '''
    theta_H1 = np.random.rand(n_feature+1)
    theta_H2 = np.random.rand(n_feature+1)
    theta_o = np.random.rand(n_feature+1)
    '''
    theta_H1 = np.array([0.8,0.5,-0.1])
    theta_H2 = np.array([0.7,0.3,-0.5])
    theta_o = np.array([0.2,0.3,0.5])  
    w_H1 = theta_H1[0:n_feature]
    b_H1 = theta_H1[n_feature]
    w_H2 = theta_H2[0:n_feature]
    b_H2 = theta_H2[n_feature]
    w_o = theta_o[0:n_feature]
    b_o = theta_o[n_feature]

    for i in range(1,batch):
        H1 = fx(x,w_H1,b_H1)
        H2 = fx(x,w_H2,b_H2)
        H = np.column_stack((H1,H2))
        o = fx(H,w_o,b_o)
        #loss_o = loss(o-y)
        delta = o-y
        Loss_o = sum(loss(delta)) / n_sample
        loss_H = []
        for hiden_w in w_o:
            loss_H.append(hiden_w * delta)

        if Loss_o < 0.00001:
            print(i)
            return [np.append(w_H1,b_H1),np.append(w_H2,b_H2),np.append(w_o,b_o)]
        g_H1 = grad(x,w_H1,b_H1,loss_H[0])
        g_H2 = grad(x,w_H2,b_H2,loss_H[1])
        g_o = grad(H,w_o,b_o,delta)
        
        #print(i,Loss_o,g_H1,g_H2,g_o)
        delta_g_H1 = -g_H1 * learning_rate
        delta_g_H2 = -g_H2 * learning_rate
        delta_g_o = -g_o * learning_rate
        w_H1 = w_H1 + delta_g_H1[0:n_feature]
        b_H1 = b_H1 + delta_g_H1[n_feature]
        w_H2 = w_H2 + delta_g_H2[0:n_feature]
        b_H2 = b_H2 + delta_g_H2[n_feature]
        w_o = w_o + delta_g_o[0:n_feature]
        b_o = b_o + delta_g_o[n_feature]
    return [np.append(w_H1,b_H1),np.append(w_H2,b_H2),np.append(w_o,b_o)]       

def predict(model,x,y):
    theta_H1,theta_H2,theta_o = model
    w_H1 = theta_H1[0:n_feature]
    b_H1 = theta_H1[n_feature]
    w_H2 = theta_H2[0:n_feature]
    b_H2 = theta_H2[n_feature]
    w_o = theta_o[0:n_feature]
    b_o = theta_o[n_feature]
    H1 = fx(x,w_H1,b_H1)
    H2 = fx(x,w_H2,b_H2)
    H = np.column_stack((H1,H2))
    o = fx(H,w_o,b_o)
    delta = o-y
    print(delta)

w_b = run_optimization(X,Y)
predict(w_b,X,Y)