#coding=utf-8

"""
    基本功能函数：
        axes 返回行轴标签列表。
        dtype 返回对象的数据类型(dtype)。
        empty 如果系列为空，则返回True。
        ndim 返回底层数据的维数，默认定义：1。
        size 返回基础数据中的元素数。
        values 将系列作为ndarray返回。
        head() 返回前n行。
        tail()  返回最后n行。


    DataFrame基本函数：
        T 转置行和列。
        axes 返回一个列，行轴标签和列轴标签作为唯一的成员。
        dtypes 返回此对象中的数据类型(dtypes)。
        empty 如果NDFrame完全为空[无项目]，则返回为True; 如果任何轴的长度为0。
        ndim 轴/数组维度大小。
        shape 返回表示DataFrame的维度的元组。
        size NDFrame中的元素数。
        values NDFrame的Numpy表示。
        head() 返回开头前n行。
        tail() 返回最后n行。

"""

import numpy as np
import pandas as pd

def f1():
    s = pd.Series(np.random.randn(6))
    print(s)
    print("=="*32)

    # 返回系列的标签列表，表示 上述结果是从0到7的值列表的紧凑格式，即：[0,1,2,3,4,5,6]
    print(s.axes)
    print("=="*32)

    #返回布尔值，表示对象是否为空
    print(s.empty)
    print("=="*32)

    # ndim 返回对象的维数。根据定义，一个系列是一个1D数据结构
    print(s.ndim)
    print("=="*32)

    # size 返回系列的大小(长度)
    print(s.size)
    print("=="*32)

    # values 以数组形式返回系列中的实际数据值
    print(s.values)
    print("=="*32)



def f2():
    d = {'Name':pd.Series(['Tom','James','Ricky','Vin','Steve','Minsu','Jack']),
        'Age':pd.Series([25,26,25,23,30,29,23]),
        'Rating':pd.Series([4.23,3.24,3.98,2.56,3.20,4.6,3.8])
        }
    df = pd.DataFrame(d)
    print(df)
    print('=='*32)

    # T 转置
    print(df.T)
    print('=='*32)

    # axes 返回行轴标签和列轴标签列表
    print(df.axes)
    print('=='*32)

    # dtypes 返回每列的数据类型
    print(df.dtypes)
    print('=='*32)

    # empty 返回布尔值，表示对象是否为空;
    print(df.empty)
    print('=='*32)

    # ndim 返回对象的维数
    print(df.ndim)
    print('=='*32)

    # shape 返回表示DataFrame的维度的元组
    print(df.shape)
    print('=='*32)

    # size 返回DataFrame中的元素数
    print(df.size)
    print('=='*32)


def f3():
    """
        将两个list合成一个DataFrame
    """
    l1 = range(1,11)
    l2 = range(101, 111)
    lall = list(zip(l1, l2))
    print(lall)
    names=['id',"predicition"]
    df = pd.DataFrame(lall, columns=names)
    print(df)









if __name__ == '__main__':
    #f1()
    #f2()
    f3()
