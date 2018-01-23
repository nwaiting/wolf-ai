#coding=utf-8

"""
参考：
http://python.jobbole.com/81721/
http://python.jobbole.com/87994/?utm_source=blog.jobbole.com&utm_medium=relatedPosts
"""

import numpy as np
import urllib
from sklearn import preprocessing
from sklearn import metrics
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

def LogisticReg():
    #url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/pima-indians-diabetes/pima-indians-diabetes.data'
    #raw_data = urllib.urlopen(url=url)
    dataset = np.loadtxt('D:\\opensource\\alg\\machine learning\\diabetes.data.1', delimiter=',')
    x = dataset[:,0:7]
    y = dataset[:,8]
    #标准化 归一化
    standardized_x = preprocessing.scale(x)
    #规则化 它包括数据的预处理，使得每个特征的值有0和1的离差
    normalized_x = preprocessing.normalize(x)

    #特征工程
    #对于特征的选取，已经有很多的算法可供直接使用。如树算法就可以计算特征的信息量
    model = ExtraTreesClassifier()
    model.fit(x, y)
    print model.feature_importances_

    #选取好的子集
    model = LogisticRegression()
    rfe = RFE(model, 3)
    rfe = rfe.fit(x, y)
    print rfe.support_
    print rfe.ranking_

    # LogisticRegression
    model = LogisticRegression()
    model.fit(x, y)
    print model
    expected = y
    predicted = model.predict(x)
    print metrics.classification_report(expected, predicted)
    print metrics.confusion_matrix(expected, predicted)

    #bayes
    from sklearn.naive_bayes import GaussianNB
    model = GaussianNB()
    model.fit(x, y)
    print model
    expected = y
    predicted = model.predict(x)
    print metrics.classification_report(expected, predicted)
    print metrics.confusion_matrix(expected, predicted)

    #knn
    from sklearn.neighbors import KNeighborsClassifier
    model = KNeighborsClassifier()
    model.fit(x, y)
    print model
    expected = y
    predicted = model.predict(x)
    print metrics.classification_report(expected, predicted)
    print metrics.confusion_matrix(expected, predicted)

    #tree
    from sklearn.tree import DecisionTreeClassifier
    model = DecisionTreeClassifier()
    model.fit(x,y)
    print model
    expected = y
    predicted = model.predict(x)
    print metrics.classification_report(expected, predicted)
    print metrics.confusion_matrix(expected, predicted)

    #svm
    from sklearn.svm import SVC
    model = SVC()
    model.fit(x, y)
    print model
    expected = y
    predicted = model.predict(x)
    print metrics.classification_report(expected, predicted)
    print metrics.confusion_matrix(expected, predicted)


if __name__ == '__main__':
    LogisticReg()
