#coding=utf-8

"""
    pandas处理三种数据结构：
        系列(Series)
            一维数据
        数据帧(DataFrame)
            2维数据
            DataFrame是Series的容器
        面板(Panel)
            3维数据
            Panel是DataFrame的容器
        这些数据结构构建在numpy数组之上，意味着它们应该很快
        除了系列都是大小可变的，系列是大小不变的


    注意：
        注意虽然用于选择和设置的标准Python/Numpy表达式是直观的，可用于交互式工作，但对于生产代码，但建议使用优化的Pandas数据访问方法.at，.iat，.loc，.iloc和.ix。
"""

import pandas as pd
import numpy as np

def main():
    # 创建对象
    s = pd.Series([1,3,5,np.nan,6,8])
    print(s)
    print("=="*16)

    dates = pd.date_range("20190101", periods=7)
    print(dates)
    print("=="*16)

    print(np.random.randn(7,4))
    print("=="*16)

    df = pd.DataFrame(np.random.randn(7,4), index=dates, columns=list('ABCD'))
    print(df)
    print("=="*16)

    df2 = pd.DataFrame({ 'A' : 1.,
                     'B' : pd.Timestamp('20170102'),
                     'C' : pd.Series(1,index=list(range(4)),dtype='float32'),
                     'D' : np.array([3] * 4,dtype='int32'),
                     'E' : pd.Categorical(["test","train","test","train"]),
                     'F' : 'foo' })
    print(df2)
    print("=="*16)

    #########################################
    # 数据文件头
    print(df.head(3))
    print("=="*16)

    # 文件尾部
    print(df.tail(3))
    print("=="*16)

    #显示索引
    print(df.index)
    print("=="*16)

    #显示列
    print(df.columns)
    print("=="*16)

    #底层numpy数据
    print(df.values)
    print("=="*16)

    #统计摘要 均值、方差等
    print(df.describe())
    print("=="*16)

    # 调换数据，类似于转置
    print(df.T)
    print("=="*16)

    ###########################
    # df.sort_index 对行、列索引进行排序
    # df.sort_values 对行、列值进行排序
    # 通过轴抽取 ascending=False 将列进行倒序输出
    print(df.sort_index(axis=1, ascending=False))
    print("=="*16)

    print(df.sort_index(axis=1, ascending=True))
    print("=="*16)

    # 通过轴抽取 ascending=False 将行进行倒序输出
    print(df.sort_index(axis=0, ascending=False))
    print("=="*16)

    print(df.sort_index(axis=0, ascending=True))
    print("=="*16)

    #按 行、列 值进行排序
    print(df.sort_values(by="B", ascending=True))
    print("=="*16)

    print(df.sort_values(axis=0, by="B", ascending=False))
    print("=="*16)

    print(df.sort_values(axis=1, by="2019-01-01", ascending=False))
    print("=="*16)

    print(df.sort_values(axis=1, by="2019-01-01", ascending=True))
    print("=="*16)


def main2():
    ###################
    # 选择区块
    dates = pd.date_range('20170101', periods=6)
    df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))
    print(df.values)
    print("=="*32)

    # 选择一列，产生一个系列，相当于df.A
    print(df['A'])
    print("=="*32)

    #选择切片
    print(df[0:3])
    print("=="*32)

    print(df['20170102':'20170103'])
    print("=="*32)

    # 按照标签选择
    # 标签获取横截面 即获取第一行数据
    print(df.loc[dates[0]])
    print("=="*32)

    # 标签选择多轴
    print(df.loc[:, ['A','B']])
    print("=="*32)
    print(df.loc[:, 'A':'B'])
    print("=="*32)

    #显示标签切片，包括两个端点
    print(df.loc['20170102':'20170104',['A','B']])
    print("=="*32)

    #减少返回对象的尺寸(大小) !!!!!!!!!!!!! 这里有点不同
    print(df.loc['20170102',['A','B']])
    print("=="*32)

    # 获得标量值
    print(df.loc[dates[0],'A'])
    print("=="*32)

    # 快速访问标量(等同于先前的方法)
    print(df.at[dates[0], 'A'])
    print("=="*32)

    ################################
    # 通过位置选择，索引从0开始，获取第几行数据
    print(df.iloc[3])
    print("=="*32)

    print(df.iloc[3:5,0:2])
    print("=="*32)

    # 要明确获取值
    print(df.iloc[1,1])
    print("=="*32)

    ######################################
    # 要快速访问标量(等同于先前的方法)
    print(df.iat[1,1])
    print("=="*32)

    #####################################
    # 布尔索引
    # 使用单列的值选择数据
    print(df[df.B>0])
    print("=="*32)

    # 从满足布尔条件的DataFrame中选择值
    print(df[df>0])
    print("=="*32)

    # 使用isin()方法进行过滤
    df2 = df.copy()
    df2['E'] = ['one', 'one','two','three','four','three']
    print(df2)
    print("=="*32)
    print(df2[df2['E'].isin(['one','two'])])


if __name__ == '__main__':
    #main()
    main2()
