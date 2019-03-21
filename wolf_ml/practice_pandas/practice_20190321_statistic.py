#coding=utf-8

"""
    统计方法有助于理解和分析数据的行为。现在我们将学习一些统计函数，可以将这些函数应用到Pandas的对象上。
    常用方法有：
        pct_change()函数
        Cov 协方差
        corr 相关性
        rank 数据排名
            # Rank可选地使用一个默认为true的升序参数; 当错误时，数据被反向排序，也就是较大的值被分配较小的排序。
            Rank支持不同的tie-breaking方法，用方法参数指定 -
                average - 并列组平均排序等级
                min - 组中最低的排序等级
                max - 组中最高的排序等级
                first - 按照它们出现在数组中的顺序分配队列
"""


import numpy as np
import pandas as pd




def main():
    s = pd.Series([1,2,3,4,5,4])
    df = pd.DataFrame(np.random.randn(8,4),index = ['a','b','c','d','e','f','g','h'], columns = ['A', 'B', 'C', 'D'])

    print(s)
    print(df)
    print("=="*32)

    # pct_change()函数： DatFrames和Panel都有pct_change()函数。此函数将每个元素与其前一个元素进行比较，并计算变化百分比。
    # 默认情况下，pct_change()对列进行操作; 如果想应用到行上，那么可使用axis = 1参数
    print(s.pct_change())
    print(df.pct_change())
    print("=="*32)


    # Cov协方差 协方差适用于系列数据。Series对象有一个方法cov用来计算序列对象之间的协方差。NA将被自动排除
    s1 = pd.Series(np.random.randn(10))
    s2 = pd.Series(np.random.randn(10))
    print(s1.cov(s2))
    print("=="*32)

    #应用于DataFrame时，协方差方法计算所有列之间的协方差(cov)值
    print(df.iloc[1])  #表示第二行
    print(df.iloc[1].cov(df.iloc[2])) #两行之间的协方差
    print("=="*32)

    print(df.ix['a'].cov(df.ix['f']))
    print("=="*32)

    # 两列的协方差
    print(df['A'].cov(df['B']))
    print("=="*32)


    # 相关性
    # 相关性显示了任何两个数值(系列)之间的线性关系。有多种方法来计算pearson(默认)，spearman和kendall之间的相关性
    print(df.ix['a'].corr(df.ix['c'], method='spearman'))
    print("=="*32)


    # 数据排名
    # 数据排名为元素数组中的每个元素生成排名。在关系的情况下，分配平均等级
    s = pd.Series(np.random.np.random.randn(5), index=list('abcde'))
    print(s)
    print("=="*32)
    s['d'] = s['b']
    print(s)
    print("=="*32)
    print(s.rank())
    print("=="*32)

















if __name__ == '__main__':
    main()
