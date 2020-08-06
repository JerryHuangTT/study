import numpy as np
import pandas as pd
'''
from activate import sigmoid_fx as Fx
from activate import sigmoid_df as DFx
'''
from activate import relu_fx as Fx
from activate import relu_df as DFx
n_hiden = 2
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

def get_layer(n_cell,n_feature):
    res = []
    for i in range(0,n_cell):
        res.append([np.random.rand(n_feature),-0.1])
    return res

def run_optimization(data):
    x = data.drop(columns=['y']).values
    y = data['y'].values
    n_feature = x.shape[1]
    w_H1 , b_H1 = np.random.rand(n_feature),-0.1
    w_H2 , b_H2 = np.random.rand(n_feature),-0.1
    w_o , b_o = np.random.rand(n_hiden),0.1

    for i in range(1,batch):
        H1 = fx(x,w_H1,b_H1)
        H2 = fx(x,w_H2,b_H2)
        H = np.column_stack((H1,H2))
        o = fx(H,w_o,b_o)
        delta = o-y
        Loss_o = sum(loss(delta)) / x.shape[0]
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
        w_o = w_o + delta_g_o[0:n_hiden]
        b_o = b_o + delta_g_o[n_hiden]

    return [np.append(w_H1,b_H1),np.append(w_H2,b_H2),np.append(w_o,b_o)]       

def predict(model,data):
    x = data.drop(columns=['y']).values
    y = data['y'].values
    n_feature = x.shape[1]
    theta_H1,theta_H2,theta_o = model
    w_H1 = theta_H1[0:n_feature]
    b_H1 = theta_H1[n_feature]
    w_H2 = theta_H2[0:n_feature]
    b_H2 = theta_H2[n_feature]
    w_o = theta_o[0:n_hiden]
    b_o = theta_o[n_hiden]

    H1 = fx(x,w_H1,b_H1)
    H2 = fx(x,w_H2,b_H2)
    H = np.column_stack((H1,H2))
    o = fx(H,w_o,b_o)
    return o

def load_data():
    data = pd.read_excel(io='basic\\0730_muti_load\\data.xlsx',sheet_name='Sheet3',header=0)
    train_data = data.sample(frac=0.8,random_state=None)
    test_data = data.drop(train_data.index)
    return train_data,test_data

batch = 1000
learning_rate = 0.01

train_data,test_data = load_data()
w_b = run_optimization(train_data)
print(test_data)
y_pred = predict(w_b,test_data)
print(y_pred)