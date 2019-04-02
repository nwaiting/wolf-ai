#coding=utf-8

"""
    fit、transform和fit_transform的区别：
        fit(): Method calculates the parameters μ and σ and saves them as internal objects.
        解释：简单来说，就是求得训练集X的均值，方差，最大值，最小值,这些训练集X固有的属性。
            fit：原义指的是安装、使适合的意思，其实有点train的含义但是和train不同的是，它并不是一个训练的过程，而是一个适配的过程，过程都是定死的，最后只是得到了一个统一的转换的规则模型。

        transform(): Method using these calculated parameters apply the transformation to a particular dataset.
        解释：在fit的基础上，进行标准化，降维，归一化等操作（看具体用的是哪个工具，如PCA，StandardScaler等）。
            transform：是将数据进行转换，比如数据的归一化和标准化，将测试数据按照训练数据同样的模型进行转换，得到特征向量。

        fit_transform(): joins the fit() and transform() method for transformation of dataset.
        解释：fit_transform是fit和transform的组合，既包括了训练又包含了转换。
        transform()和fit_transform()二者的功能都是对数据进行某种统一处理（比如标准化~N(0,1)，将数据缩放(映射)到某个固定区间，归一化，正则化等）
            fit_transform：可以看做是fit和transform的结合，如果训练阶段使用fit_transform，则在测试阶段只需要对测试样本进行transform就行了
"""

import numpy as np
from sklearn.preprocessing import MinMaxScaler,StandardScaler

def main():
    X_train = np.array([[ 1., -1.,  2.],
                        [ 2.,  0.,  0.],
                        [ 0.,  1., -1.]])
    ############ 归一化
    stand_scaler = StandardScaler()
    print(stand_scaler)
    #print(help(stand_scaler))
    print(stand_scaler.fit(X_train))
    print("=="*32)

    print("transform=",stand_scaler.transform(X_train))
    print("=="*32)

    print("fit_transform=",stand_scaler.fit_transform(X_train))
    print("=="*64)

    data = [[0, 0], [0, 0], [1, 1], [1, 1]]
    scaler = StandardScaler()
    # 对原始数据进行拟合
    print(scaler.fit(data))
    print(scaler.mean_)

    # 对数据进行某种统一的处理
    print(scaler.transform(data))
    print(scaler.transform([[2, 2]]))


















if __name__ == '__main__':
    main()
