#coding=utf-8

"""
    一般来说，这些方法采用轴参数，就像ndarray.{sum，std，...}，但轴可以通过名称或整数来指定：
        数据帧(DataFrame) - “index”(axis=0，默认)，columns(axis=1)

    常用统计：
        count() 非空观测数量
        sum() 所有值之和
        mean() 所有值的平均值
        median() 所有值的中位数
        mode() 值的模值
        std() 值的标准偏差
        min() 所有值中的最小值
        max() 所有值中的最大值
        abs() 绝对值
        prod() 数组元素的乘积
        cumsum() 累计总和
        cumprod() 累计乘积
    注意：
        由于DataFrame是异构数据结构。通用操作不适用于所有函数。
        类似于：sum()，cumsum()函数能与数字和字符(或)字符串数据元素一起工作，不会产生任何错误。字符聚合从来都比较少被使用，虽然这些函数不会引发任何异常。
        由于这样的操作无法执行，因此，当DataFrame包含字符或字符串数据时，像abs()，cumprod()这样的函数会抛出异常。
"""

import numpy as np
import pandas as pd

def main():
    d = {'Name':pd.Series(['Tom','James','Ricky','Vin','Steve','Minsu','Jack','Lee','David','Gasper','Betina','Andres']),
        'Age':pd.Series([25,26,25,23,30,29,23,34,40,30,51,46]),
        'Rating':pd.Series([4.23,3.24,3.98,2.56,3.20,4.6,3.8,3.78,2.98,4.80,4.10,3.65])
        }
    df = pd.DataFrame(d)
    print(df)
    print('=='*32)

    """
        object - 汇总字符串列
        number - 汇总数字列
        all - 将所有列汇总在一起(不应将其作为列表值传递)
    """
    print(df.describe())
    print('=='*32)

    print(df.describe(include="all"))
    print('=='*32)

    print(df.describe(include=['object']))
    print('=='*32)

    # mean
    print(df.mean(axis=0))
    print('=='*32)

    # 按照行计算平均值
    print(df.mean(1))
    print('=='*32)

    #计算某一列平均值
    print(df.loc[:, 'Age'].mean())
    print('=='*32)

if __name__ == '__main__':
    main()
