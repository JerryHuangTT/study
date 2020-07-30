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
    return Fx(y)

def loss(delta):
    return delta**2/2

def grad(x,w,b,loss):
    n_sample = x.shape[0]
    df = DFx(fx(x,w,b))
    dv = np.column_stack((x,np.ones(n_sample)))
    print(np.dot(loss*df,dv))
    return np.dot(loss*df,dv)

def main():
    x = np.array(
        [[1,2],
        [2,3],
        [3,4]])
    y = np.array([5.5,8.7,11.9])
    n_sample = x.shape[0]
    n_feature = x.shape[1]
    #theta = np.random.rand(n_feature+1)
    theta_H1 = np.array([1,1,-0.5])
    theta_H2 = np.array([1,1,-0.5])
    thet_o = np.array([1,1,-0.5])
    w_H1 = theta_H1[0:n_feature]
    b_H1 = theta_H1[n_feature]
    w_H2 = theta_H2[0:n_feature]
    b_H2 = theta_H2[n_feature]
    w_o = thet_o[0:n_feature]
    b_o = thet_o[n_feature]

    for i in range(1,batch):
        H1 = fx(x,w_H1,b_H1)
        H2 = fx(x,w_H2,b_H2)
        H = np.column_stack((H1,H2))
        o = fx(H,w_o,b_o)
        loss_o =  sum(loss(o-y)) / n_sample
        loss_H = w_o * loss_o

        if loss_o < 0.01:
            return
        g_H1 = grad(x,w_H1,b_H1,loss_H[0])
        g_H2 = grad(x,w_H2,b_H2,loss_H[1])
        g_o = grad(H,w_o,b_o,loss_o)
        #grad = 节点误差*节点导数*输入特征
        print(loss_o,g_H1,g_H2,g_o)
        delta_g_H1 = g_H1 * learning_rate
        delta_g_H2 = g_H2 * learning_rate
        delta_g_o = g_o * learning_rate
        w_H1 = w_H1 + delta_g_H1[0:n_sample-2]
        b_H1 = b_H1 + delta_g_H1[n_sample-1]
        w_H2 = w_H2 + delta_g_H2[0:n_sample-2]
        b_H2 = b_H2 + delta_g_H2[n_sample-1]
        w_o = w_o + delta_g_o[0:n_sample-2]
        b_o = b_o + delta_g_o[n_sample-1]                

main()