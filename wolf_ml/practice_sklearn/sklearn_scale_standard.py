#coding=utf-8


"""
    scale：
        标准化
        公式为：(X-mean)/std
    StandardScaler：
        标准化
        (x-u)/δ
    MinMaxScaler：
        最小－最大规范化，即归一化
        将属性缩放到一个指定的最小和最大值（通常是0-1）之间
        (x-MinValue) / (MaxValue-MinValue)
    normalize：
        正则化
        该方法主要应用于文本分类和聚类中。例如，对于两个TF-IDF向量的l2-norm进行点积，就可以得到这两个向量的余弦相似性
    Normalizer:
        正则化
"""

import numpy as np
from sklearn.preprocessing import scale,StandardScaler,MinMaxScaler,normalize,Normalizer


def main():
    X_train = np.array([[ 1., -1.,  2.],
                        [ 2.,  0.,  0.],
                        [ 0.,  1., -1.]])
    ############ 归一化
    min_max_scaler = MinMaxScaler()
    print(min_max_scaler)
    #print(help(min_max_scaler))
    #X_train_minmax = min_max_scaler.fit(X_train)
    #print(X_train_minmax.transform(X_train))
    print(min_max_scaler.fit_transform(X_train))
    print("=="*64)

    ############ 标准化
    scaler = StandardScaler()
    print(scaler)
    scaler.fit(X_train)
    print(scaler.mean_)
    #print(help(scaler))
    print(scaler.var_)
    print(scaler.transform(X_train))












if __name__ == '__main__':
    main()
