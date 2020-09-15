import pandas as pd
import numpy as np
from imblearn.over_sampling import SMOTE

def load_data():
    data = pd.read_excel('tf2\\classification\\0812\\pump.xlsx')
    i = 0
    for l in data['type'].value_counts().index:
        data.loc[data['type'] == l] = i
        i += 1    
    smo = SMOTE(random_state=42)
    n = data.shape[1]-1
    x,y = data.iloc[:,0:n], data.iloc[:,n]
    x1,y1 = smo.fit_sample(x,y)
    x1.insert(x1.shape[1], 'e', y1)
    data = x1
    print(data['e'].value_counts())

    train_data = data.sample(frac=0.9,random_state=None)
    test_data = data.drop(train_data.index)
    return train_data.values,test_data.values
     
load_data()
print('prepare datasets...')
#读取数据

raw_data = pd.read_csv('filtered_UTC8erfenlei.csv', header=0,
                       encoding="unicode_escape")
# raw_data = pd.read_csv('filtered_UTC8erfenlei.csv', header=0)
# 读取csv数据，并将第一行视为表头，返回DataFrame类型
data = raw_data.values
#smote采样
features0 = data[::, 1::]
labels0 = data[::, 0]
smo = SMOTE(random_state=42)
features, labels = smo.fit_sample(features0, labels0)

print(Counter(labels0))
print(labels)
print(Counter(labels))

# 选取0.3%数据作为测试集，剩余为训练集

train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.3,
                                                                             random_state=0)