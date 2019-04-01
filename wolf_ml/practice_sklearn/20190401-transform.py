#coding=utf-8

"""
    fit、transform和fit_transform的区别：
        fit(): Method calculates the parameters μ and σ and saves them as internal objects.
        解释：简单来说，就是求得训练集X的均值，方差，最大值，最小值,这些训练集X固有的属性。

        transform(): Method using these calculated parameters apply the transformation to a particular dataset.
        解释：在fit的基础上，进行标准化，降维，归一化等操作（看具体用的是哪个工具，如PCA，StandardScaler等）。

        fit_transform(): joins the fit() and transform() method for transformation of dataset.
        解释：fit_transform是fit和transform的组合，既包括了训练又包含了转换。
        transform()和fit_transform()二者的功能都是对数据进行某种统一处理（比如标准化~N(0,1)，将数据缩放(映射)到某个固定区间，归一化，正则化等）
"""


def main():
    pass





if __name__ == '__main__':
    main()
