# coding=utf-8


import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import Lasso, LassoCV
from sklearn.linear_model import Ridge
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


"""
    数据参考：http://archive.ics.uci.edu/ml/machine-learning-databases/00294/
"""

def load_data():
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "CCPP", "Folds5x2_pp.xlsx")
    df = pd.read_excel(file_path, sheetname="Sheet1")
    y = df.PE
    X = df.values[:, 0:-1]
    return X, y


def linear_lasso():
    model = Lasso(alpha=0.01)
    model = LassoCV(alphas=[0.01, 0.1, 0.5, 1, 3, 5, 7, 10, 20, 100])
    # LassoCV()  # LassoCV自动调节alpha可以实现选择最佳的alpha
    X, y = load_data()
    model.fit(X, y)
    #plt.scatter(X, y, c='r')
    #plt.show()
    print("lasso result ", model.coef_)
    print("lasso best alpha ", model.alpha_)


def linear_ridge():
    model = Ridge(alpha=0.01)
    X, y = load_data()
    model.fit(X, y)
    #plt.scatter(X, y, c='b')
    #plt.show()
    print("ridge result ", model.coef_)

def linear_ridge2():
    X = 1. / (np.arange(1, 11) + np.arange(0, 10)[:, np.newaxis])
    y = np.ones(10)
    n_alphas = 200
    # alphas count is 200, 都在10的-10次方和10的-2次方之间
    alphas = np.logspace(-10, -2, n_alphas)
    clf = Ridge(fit_intercept=False)
    coefs = []
    # 循环200次
    for a in alphas:
        # 设置本次循环的超参数
        clf.set_params(alpha=a)
        # 针对每个alpha做ridge回归
        clf.fit(X, y)
        # 把每一个超参数alpha对应的theta存下来
        coefs.append(clf.coef_)
    ax = plt.gca()

    ax.plot(alphas, coefs)
    # 将alpha的值取对数便于画图
    ax.set_xscale('log')
    # 翻转x轴的大小方向，让alpha从大到小显示
    ax.set_xlim(ax.get_xlim()[::-1])
    plt.xlabel('alpha')
    plt.ylabel('weights')
    plt.title('Ridge coefficients as a function of the regularization')
    plt.axis('tight')
    plt.show()


if __name__ == "__main__":
    #linear_lasso()
    #linear_ridge()
    linear_ridge2()

