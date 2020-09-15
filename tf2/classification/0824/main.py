import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn import preprocessing
from imblearn.over_sampling import SMOTE

num_class = 0
num_feature = 0

def load_data():
    global num_class,num_feature
    data = pd.read_csv('tf2\\classification\\0824\\pump.csv')
    print(data['type'].value_counts())
    num_class = data['type'].value_counts().shape[0]
    train_data = data.sample(frac=0.7,random_state=None)
    test_data = data.drop(train_data.index)
    num_feature = train_data.shape[1]-1
    '''
    x,y = train_data.iloc[:,0:num_feature], train_data.iloc[:,num_feature]
    smo = SMOTE(random_state=42)
    ex_x,ex_y = smo.fit_sample(x,y)
    ex_x.insert(ex_x.shape[1], 'type', ex_y)
    train_data = ex_x
    '''
    print(train_data['type'].value_counts())
    print(test_data['type'].value_counts())
    return train_data.values,test_data.values

def parse_data():
    train_data,test_data = load_data()
    n = num_feature
    x_train = preprocessing.scale(train_data[:,0:n])
    y_train = np.float32(tf.keras.utils.to_categorical(train_data[:,n],num_class))
    x_test = preprocessing.scale(test_data[:,0:n])
    y_test =  np.float32(tf.keras.utils.to_categorical(test_data[:,n],num_class))
    return (x_train, y_train), (x_test, y_test)

(x_train, y_train), (x_test, y_test) = parse_data()

input_x = tf.keras.Input(shape=(num_feature),name='input_x')
h1_l = tf.keras.layers.Dense(64, activation=tf.nn.relu,name='h1_1')(input_x)
h2_l = tf.keras.layers.Dense(32, activation=tf.nn.relu,name='h2_1')(h1_l)
h3_l = tf.keras.layers.Dense(16, activation=tf.nn.relu,name='h3_1')(h2_l)
output_y = tf.keras.layers.Dense(num_class, activation=tf.nn.softmax,name='output_y')(h3_l)
model = tf.keras.Model(inputs=input_x,outputs=output_y)


model.compile(optimizer=tf.optimizers.Adam(1e-3),
                loss=tf.losses.categorical_crossentropy,
                metrics=['acc'])
model.fit(x=x_train,y=y_train,
            batch_size=128,epochs=50)
score = model.evaluate(x_test,y_test)
model.save('no_smote_no_normal.h5')