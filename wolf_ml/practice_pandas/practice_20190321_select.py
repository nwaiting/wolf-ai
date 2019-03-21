#coding=utf-8


"""
    Python和NumPy索引运算符"[]"和属性运算符"."。 可以在广泛的用例中快速轻松地访问Pandas数据结构。然而，由于要访问的数据类型不是预先知道的，所以直接使用标准运算符具有一些优化限制。对于生产环境的代码，我们建议利用本章介绍的优化Pandas数据访问方法
    Pandas现在支持三种类型的多轴索引：
        .loc() 基于标签
            .loc()具有多种访问方式，如 -
                单个标量标签
                标签列表
                切片对象
                一个布尔数组

        .iloc() 基于整数
            Pandas提供了各种方法，以获得纯整数索引。像python和numpy一样，第一个位置是基于0的索引。
            各种访问方式如下 -
                整数
                整数列表
                系列值

        .ix() 基于标签和整数
            除了基于纯标签和整数之外，Pandas还提供了一种使用.ix()运算符进行选择和子集化对象的混合方法。

"""

import numpy as np
import pandas as pd


def main1():
    # .loc()
    df = pd.DataFrame(np.random.randn(8, 4),index = ['a','b','c','d','e','f','g','h'], columns = ['A', 'B', 'C', 'D'])
    print(df)
    print("=="*32)

    # 两种返回的数据上面有列标签，下面没有列标签
    print(df.loc[:,['A']])
    print(df.loc[:,'A'])
    print("=="*32)

    print(df.loc[:,['A','C']])
    print("=="*32)

    print(df.loc[['a'],['A']])
    print("=="*32)

    # 取行值
    print(df.loc['a']>0)
    print("=="*32)

    # 取列值
    print(df.loc[:,['A']]>0)
    print("=="*32)

    # error !!!!!!!!!!!!!!!!!!!!!!!!! 下面写法是错误的
    #print(df.loc[:4])
    # print(df.loc[:4,:])
    print("=="*32)

def main2():
    # .iloc
    df = pd.DataFrame(np.random.randn(8, 4),index = ['a','b','c','d','e','f','g','h'], columns = ['A', 'B', 'C', 'D'])
    print(df)
    print('=='*32)

    print(df.iloc[:4])
    print('=='*32)

    print(df.iloc[:,:2])
    print('=='*32)

    print(df.iloc[[1, 3, 5], [1, 3]])
    print('=='*32)

    print(df.loc['a']>0)
    print("=="*32)

    print(df.loc[['a'],['A']])
    print("=="*32)

def main3():
    # .lx
    df = pd.DataFrame(np.random.randn(8, 4),index = ['a','b','c','d','e','f','g','h'], columns = ['A', 'B', 'C', 'D'])
    print(df)
    print('=='*32)

    print(df.ix[:4])
    print('=='*32)

    print(df.ix[:,'A'])
    print('=='*32)

def main4():
    # 直接访问
    df = pd.DataFrame(np.random.randn(8, 4),index = ['a','b','c','d','e','f','g','h'], columns = ['A', 'B', 'C', 'D'])
    print(df)
    print('=='*32)

    # 两个有的区别
    print(df['A'])
    print(df[['A']])
    print('=='*32)

    print(df[['A','B']])
    print('=='*32)

    print(df[2:2])
    print('=='*32)

    print(df.A)
    print('=='*32)

    print(df.index)
    print('=='*32)

    # 获取某一行
    print(df.iloc[0])
    print('=='*32)

if __name__ == '__main__':
    #main1()
    #main2()
    #main3()
    main4()
