#coding=utf-8

from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor

def decision_tree_classify():
    x = [[0,0], [1,0], [0,1], [3,2], [4,7], [0,8]]
    y = [0,0,0,1,1,0]
    clf = DecisionTreeClassifier()
    clf = clf.fit(x,y)
    #预测分类
    print clf.predict([[2, 5]])
    #每个分类的概率可以被预测，即某个叶子中，该分类样本的占比
    print clf.predict_proba([[3, 4]])
    print "decision tree"

def decision_tree_regression():
    print "regression"
    x = [[0,0,0],[1,1,1],[2,2,2]]
    y = [0.5, 1.5, 2.5]
    rgs = DecisionTreeRegressor()
    rgs = rgs.fit(x,y)
    print rgs.predict([[1.5,1.5,1.5]])

if __name__ == '__main__':
    #decision_tree_classify()
    #decision_tree_regression()
