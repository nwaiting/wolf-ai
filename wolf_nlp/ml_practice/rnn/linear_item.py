#coding=utf-8

"""
    用感知器实现一个线性分类器
    注：
        1、感知器有一个问题，当面对的数据集不是线性可分的时候，感知器规则可能无法收敛，这意味着我们永远无法完成一个感知器的训练
            解决方法：使用一个可导的线性函数来替代感知器的阶跃函数，这种感知器就叫做线性单元
            替换激活函数后，线性单元将返回一个实数值而不是0,1分类。因此线性单元用来解决回归问题，而不是分类问题。

    感知器模型和线性单元模型：
        训练规则相同
        模型中，仅激活函数不同
"""

from percepron import Perceptron

class LinearUnit(Perceptron):
    def __init__(self, in_num):
        Perceptron.__init__(self, in_num=in_num)
    def f(self, x):
        return x


def get_train_data():
    in_vec = [[5],[3],[8],[1.5],[10]]
    labels = [5500, 2300, 7600, 1800, 11400]
    return in_vec,labels

def train_linear_unit():
    










if __name__ == '__main__':
    main()
