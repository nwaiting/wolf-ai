#coding=utf-8

"""
一元线性回归
LinearRegression的fit()方法就是学习这个一元线性回归模型：y = a + bx
"""
from sklearn.linear_model import LinearRegression

def linear_regression():
    x_train = [[1],[3],[3],[4],[5],[6]]
    y_ = [[1],[2.1],[2.9],[4.2],[5.1],[5.8]]
    lr = LinearRegression()
    lr.fit(x_train, y_)
    print lr.predict([13])

    #求解多元线性回归
    x_train = [[1,1,1],[1,1,2],[1,2,1]]
    y_train = [[6],[9],[8]]
    lr.fit(x_train, y_train)
    print lr.predict([1,3,5])

if __name__ == '__main__':
    linear_regression()
