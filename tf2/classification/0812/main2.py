import numpy as np
import pandas as pd

def load_data():
    data = pd.read_excel('tf2\\classification\\0812\\pump.xlsx')
    train_data = data.sample(frac=0.7,random_state=None)
    test_data = data.drop(train_data.index)
    return train_data,test_data

def one_hot(data):
    #x = data.iloc[:,0:data.shape[1]-1]
    data['type'] = data['type'].astype('object')
    print(data['type'].value_counts())
    data_dummies = pd.get_dummies(data)
    print(list(data_dummies.columns))
    return data_dummies

train_data,test_data = load_data()
one_hot_train_data = one_hot(train_data)
one_hot_test_data = one_hot(test_data)
