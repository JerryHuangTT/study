import numpy as np
import matplotlib.pyplot as plt

a1 = np.array([[1,2],[3,4]])
a2 = np.array([[1,1],[2,2]])
print(np.dot(a1,a2))


##使用iris数据作为测试数据，需要将数据文件'iris.data'放置在此文件的目录下
iris = []
target = []
with open('basic\\0805\\data.csv') as f:
    for line in f.readlines():
        iris.append(line.strip().split(',')[0:4])
        target.append(['Iris-setosa'==line.strip().split(',')[4],
                       'Iris-versicolor'==line.strip().split(',')[4],'Iris-virginica'==line.strip().split(',')[4]])
iris = np.array(iris).astype(float)
target=np.array(target)

def softmax(x_train,y_train):
    cost_trend = []
    alpha = 3*10**(-3)
    max_iter = 3*10**4
    tol = 0.05
    
    x_train = np.hstack((np.ones(x_train.shape[0]).reshape(x_train.shape[0],1),x_train))
    M,N = x_train.shape
    K = y_train.shape[1]
    omg = np.array([[1,1,1],
    [1,1,1],
    [-1,-1,-1],
    [-1,-1,-1],
    [0.5,0.5,0.5]])
    for i in range(max_iter):
        t = np.exp(x_train@omg)
        grad = x_train.T.dot(t/(t.sum(axis=1)).reshape(M,1) - y_train)
        omg -= alpha*grad
        cost = -(np.log(t / (t.sum(axis=1).reshape(M,1))) * y_train).sum()
        if i in range(0,max_iter,200):
            #print(cost)
            cost_trend.append([i,cost])

        if cost/M <tol:
            return omg,cost,cost_trend
    print('达到最大迭代步数，但模型尚未收敛到指定精度')    
    return omg,cost,cost_trend
def pred(x,omg):
    x = np.hstack((np.ones(x.shape[0]).reshape(x.shape[0],1),x))
    return np.exp(x@omg)/np.exp(x@omg).sum(axis=1).reshape(x.shape[0],1)

omg,meanerror,error = softmax(iris,target)
pred = pred(iris,omg)
print('模型在测试数据上的错误率为{:.2f}%'.format(float(sum(abs(pred.argmax(axis=1)-target.argmax(axis=1)))/150)*100)) 
plt.plot([item[0] for item in error[2:]],[item[1]for item in error[2:]])
plt.title('cost-iteration')
plt.show()