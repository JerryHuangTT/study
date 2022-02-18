import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE,BorderlineSMOTE
from matplotlib import pyplot as plt
import tensorflow as tf
num_class = 4
num_feature = 6

# 27648 正常工况 0
# 30720 支架固定螺栓松动 1
# 2048  汽蚀工况 3
# 25600 泵脚及支架螺栓同时松动 2

df = pd.read_csv(r'tf2\classification\0915\pump.csv')

# 1.缺失值判断以及数据分布绘图
# print(df.isnull().value_counts())
# ax = df['type'].value_counts(normalize=True).plot(kind='bar',title='label distribution')
# ax.set_ylabel('Proportion of labels')
# ax.set_xlabel('Labels')
# plt.show()

# 2.由于数据量多，做随机抽样1%，2维特征，2类标签可视化
tmp = df.sample(frac=0.01,random_state=None)
plt.scatter(tmp[tmp['type']==3]['y1'], tmp[tmp['type']==3]['y2'],label="Minority class")
plt.scatter(tmp[tmp['type']==1]['y1'], tmp[tmp['type']==1]['y2'],label="Majority class")
plt.legend(loc='best')
plt.show()

# 3.split测试集和训练集
train_data = df.sample(frac=0.7,random_state=None)
test_data = df.drop(train_data.index)

# sm2 = BorderlineSMOTE(random_state=42,kind='borderline-2')
# ex_x2,ex_y2 = sm2.fit_sample(x,y)
# ex_x2.insert(ex_x2.shape[1], 'type', ex_y2)

# 5.由于数据量多，做随机抽样1%，2维特征，2类标签可视化
# tmp = ex_x2.sample(frac=0.01,random_state=None)
# plt.scatter(tmp[tmp['type']==3]['y1'], tmp[tmp['type']==3]['y2'],label="Minority class")
# plt.scatter(tmp[tmp['type']==1]['y1'], tmp[tmp['type']==1]['y2'],label="Majority class")
# plt.legend(loc='best')
# plt.title("BorderlineSMOTE")
# plt.show()


train,test = train_data.values,test_data.values
x_test = test[:,0:num_feature]
y_test =  np.float32(tf.keras.utils.to_categorical(test[:,num_feature],num_class))
x_train = train[:,0:num_feature]
y_train = np.float32(tf.keras.utils.to_categorical(train[:,num_feature],num_class))

input_x = tf.keras.Input(shape=(num_feature))
h1_l = tf.keras.layers.Dense(64, activation=tf.nn.relu)(input_x)
h2_l = tf.keras.layers.Dense(32, activation=tf.nn.relu)(h1_l)
h3_l = tf.keras.layers.Dense(16, activation=tf.nn.relu)(h2_l)
output_y = tf.keras.layers.Dense(num_class, activation=tf.nn.softmax)(h3_l)
model = tf.keras.Model(inputs=input_x,outputs=output_y)

model.compile(optimizer=tf.train.AdamOptimizer(1e-3),
                loss='categorical_crossentropy',
                metrics=['acc'])
model.fit(x=x_train,y=y_train,
            batch_size=128,epochs=50)
score = model.evaluate(x_test,y_test)
model.save('no_smote.h5')

sm = SMOTE(random_state=42)
x,y = train_data.iloc[:,0:num_feature], train_data.iloc[:,num_feature]
ex_x,ex_y = sm.fit_sample(x,y)
ex_x.insert(ex_x.shape[1], 'type', ex_y)
train = ex_x.values
x_train = train[:,0:num_feature]
y_train = np.float32(tf.keras.utils.to_categorical(train[:,num_feature],num_class))

modle1 = tf.keras.Model(inputs=input_x,outputs=output_y)
modle1.compile(optimizer=tf.train.AdamOptimizer(1e-3),
                loss='categorical_crossentropy',
                metrics=['acc'])
modle1.fit(x=x_train,y=y_train,
            batch_size=128,epochs=50)
score1 = modle1.evaluate(x_test,y_test)
modle1.save('smote.h5')