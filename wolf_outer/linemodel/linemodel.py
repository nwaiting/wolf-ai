#coding=utf-8

from sklearn.linear_model import LinearRegression
from sklearn.linear_model.logistic import LogisticRegression, LogisticRegressionCV
# LogisticRegression和LogisticRegressionCV区别：
# LogisticRegression 需要自己指定一个正则化系数
# LogisticRegressionCV 使用交叉验证来选择正则化系数
from sklearn import datasets
from matplotlib import pyplot as plt
from sklearn.cross_validation import train_test_split

def func1():
    # n_features 设置多少个特征，多维的特征
    # n_informative 有几个属性是有特别关联的
    # n_targets 有多少个输出
    #X,y = datasets.make_regression(n_samples=100, n_features=100, n_informative=10, n_targets=1, noise=0.0, bias=0.0, random_state=None)
    X,y = datasets.make_regression(n_samples=10, n_features=2)

    print('line X ', X)
    print('line y ', y)

    #plt.scatter(X[:,0],y)
    #plt.show()


    lm = LinearRegression()
    lm.fit(X,y)
    X_test = [[0.69803203,0.62000084]]
    y_predict = lm.predict(X_test)
    print(y_predict)


    X,y = datasets.make_moons(10, noise=0.2)
    print('logis ', X)
    print('logis ', y)
    #X_train,X_test,y_train,y_test = train_test_split(X,y)
    logis_regre = LogisticRegression()
    #y = [[-140.66643209],[114.7982953],[103.11834249],[-177.27466722],[24.48139711],[-30.44916242],[38.96288527],[-57.62121771],[82.14111136],[90.54966151]]
    logis_regre.fit(X,y)
    print(logis_regre.predict(X_test))

    logis_regre = LogisticRegressionCV()
    logis_regre.fit(X,y)
    print(logis_regre.predict(X_test))

if __name__ == '__main__':
    func1()
