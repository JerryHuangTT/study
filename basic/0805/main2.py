import numpy as np
import matplotlib.pyplot as plt

iris = []
target = []
with open('basic\\0805\\data.csv') as f:
    for line in f.readlines():
        iris.append(line.strip().split(',')[0:4])
        target.append(['Iris-setosa'==line.strip().split(',')[4],
                       'Iris-versicolor'==line.strip().split(',')[4],'Iris-virginica'==line.strip().split(',')[4]])

iris = np.array(iris).astype(float)
target=np.array(target)
learning_rate = 0.003
max_iter = 100000

def softmax(x_train,y_train):
    n_sample = x_train.shape[0]
    #X = np.column_stack((x_train,np.ones(n_sample)))
    X = np.hstack((np.ones(x_train.shape[0]).reshape(x_train.shape[0],1),x_train))
    n_feature = X.shape[1]
    n_class = y_train.shape[1]
    H_theta = np.random.rand(n_class*n_feature).reshape(n_feature,n_class)
    for i in range(max_iter):
        H = np.dot(X,H_theta)
        H_soft = np.exp(H)
        O = H_soft / H_soft.sum(axis=1).reshape(n_sample,1) 
        grad = X.T.dot(O-y_train)
        H_theta -= learning_rate * grad
        cost = -(np.log(O) * y_train).sum() / n_sample
        if i in range(0,max_iter,200):
            a = 0
            #print(grad)
            #print(cost)
        if cost < 0.043:
            return H_theta

def pred(x,omg):
    x = np.hstack((np.ones(x.shape[0]).reshape(x.shape[0],1),x))
    return np.exp(x@omg)/np.exp(x@omg).sum(axis=1).reshape(x.shape[0],1)

m = [[0,'Iris-setosa'],
[1,'Iris-versicolor'],
[2,'Iris-virginica']]
def to_label(indexs):
    labels = []
    for i in indexs:
        l = m[i][1]
        print(l)
        labels.append(l)
    return labels

theta = softmax(iris,target)
pred = pred(iris,theta)
res = to_label(pred.argmax(axis=1))


print('模型在测试数据上的错误率为{:.2f}%'.format(float(sum(abs(pred.argmax(axis=1)-target.argmax(axis=1)))/150)*100)) 
plt.plot([item[0] for item in error[2:]],[item[1]for item in error[2:]])
plt.title('cost-iteration')
plt.show()