#coding=utf-8

"""
    transform详解：
        transform方法主要用来对特征进行转换。从可利用信息的角度来说，转换分为无信息转换和有信息转换。
            无信息转换是指不利用任何其他信息进行转换，比如指数、对数函数转换等。
            有信息转换从是否利用目标值向量又可分为无监督转换和有监督转换。
                无监督转换指只利用特征的统计信息的转换，统计信息包括均值、标准差、边界等等，比如标准化、PCA法降维等。
                有监督转换指既利用了特征信息又利用了目标值信息的转换，比如通过模型选择特征、LDA法降维等
    fit详解：
        只有有信息的转换类的fit方法才实际有用，显然fit方法的主要工作是获取特征信息和目标值信息，在这点上，fit方法和模型训练时的fit方法就能够联系在一起了：
        都是通过分析特征和目标值，提取有价值的信息，
            对于转换类来说是某些统计量，
            对于模型来说可能是特征的权值系数等。
        另外注意：只有有监督的转换类的fit和transform方法才需要特征和目标值两个参数。
            fit方法无用不代表其没实现，而是除合法性校验以外，其并没有对特征和目标值进行任何处理，

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
