# encoding=utf-8
# -*- coding : utf-8-*-
# coding:unicode_escape
print(1)

__author__ = '徐贝贝'
import time
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import svm
from imblearn.over_sampling import SMOTE
from collections import Counter
import joblib
from sklearn import metrics
import math


print('prepare datasets...')
raw_data = pd.read_csv('pump_test.csv', header=0,
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
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.3,	
	random_state=0)
	
#进行模型训练
time_2 = time.time()
print('模型训练中...')
 #SVM分类
clf = svm.SVC()
clf.fit(train_features, train_labels)
time_3 = time.time()

print('训练耗时 %f s' % (time_3 - time_2))
# joblib.dump(clf, 'save/clf2.pkl',protocol=2) #保存模型
with open('clf2.pkl', 'wb') as f:
	joblib.dump(clf, f, protocol=2)

'''
#进行模型测试
print('模型测试中...')
test_predict = clf.predict(test_features)
#print(test_predict)
time_4 = time.time()
print('测试耗时 %f s' % (time_4 - time_3))

#以下工作为输出测试结果

Accuracy = metrics.accuracy_score(test_labels, test_predict)
tn, fp, fn, tp = metrics.confusion_matrix(test_labels, test_predict, labels=[0, 1]).ravel()
F1measure = metrics.f1_score(test_labels, test_predict, labels=None, pos_label=1, average='binary', sample_weight=None)
Sensitivity = metrics.recall_score(test_labels, test_predict, labels=None, pos_label=1,average='binary', sample_weight=None)
Specificity = tn / (tn + fp)
Gmeans = math.sqrt(Sensitivity * Specificity)
print("Sensitivity= %f" % Sensitivity)
print("Specificity = %f" % Specificity)
print("*" * 8, "Testing Results", "*" * 8) 
print("准确率是： %f" % Accuracy)
print("F1-measure = %f" % F1measure)
print("G-means = %f" % Gmeans)
'''