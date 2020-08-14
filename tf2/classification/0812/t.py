import time
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import svm
from imblearn.over_sampling import SMOTE
from collections import Counter
from sklearn.externals import joblib #jbolib模块
from sklearn import metrics
import math

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