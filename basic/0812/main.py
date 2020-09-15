import numpy as np
import pandas as pd

def softmax(x_train,y_train):
    learning_rate = 0.003
    max_iter = 100000    
    n_sample = x_train.shape[0]
    X = np.column_stack((x_train,np.ones(n_sample)))#任意扩展一列 做b
    n_feature = X.shape[1]
    n_class = y_train.shape[1]
    H_theta = np.random.rand(n_class*n_feature).reshape(n_feature,n_class)
    for i in range(max_iter):
        H = np.dot(X,H_theta)
        H_soft = np.exp(H)
        O = H_soft / H_soft.sum(axis=1).reshape(n_sample,1)
        grad = X.T.dot(O-y_train)
        H_theta -= learning_rate * grad
        cost = -(np.log(O) * y_train).sum().sum() / n_sample
        #print( (np.log(O) * y_train).shape)
        #print( (np.log(O) * y_train).sum(axis=1))
        if i in range(0,max_iter,1000):
            #print(grad)
            if cost<4 and i > 2000:
                print(i,cost)
                return H_theta

def pred(x,omg):
    n_sample = x.shape[0]
    x = np.column_stack((x,np.ones(n_sample)))#任意扩展一列 做b
    return np.exp(x@omg)/np.exp(x@omg).sum(axis=1).reshape(x.shape[0],1)

def load_data():
    data = pd.read_csv('basic\\0812\\pump.csv')
    data = data.sample(frac=0.1,random_state=None)
    train_data = data.sample(frac=0.7,random_state=None)
    test_data = data.drop(train_data.index)
    return train_data,test_data

def one_hot(data):
    data['type'] = data['type'].astype('object')
    print(data['type'].value_counts().sort_index())
    data_dummies = pd.get_dummies(data,prefix=['jerry'],columns=['type'])
    print(list(data_dummies.columns))
    return data_dummies

train_data,test_data = load_data()
n_x = train_data.shape[1]-1
one_hot_train_data = one_hot(train_data)
one_hot_test_data = one_hot(test_data)
n_x_hot = one_hot_train_data.shape[1]

theta = softmax(one_hot_train_data.iloc[:,0:n_x],
                one_hot_train_data.iloc[:,n_x:n_x_hot])

y_test = one_hot_test_data.iloc[:,n_x:n_x_hot]
y_pred = pred(one_hot_test_data.iloc[:,0:n_x],theta)


label_test = y_test.values().argmax(axis=1)
label_pred = y_pred.argmax(axis=1)
acc = label_test - label_pred
print( np.sum(acc== 0) / acc.shape[0])