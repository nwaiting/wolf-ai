#coding=utf-8


"""
    重新索引会更改DataFrame的行标签和列标签。重新索引意味着符合数据以匹配特定轴上的一组给定的标签。
    可以通过索引来实现多个操作 -
        重新排序现有数据以匹配一组新的标签。
        在没有标签数据的标签位置插入缺失值(NA)标记
"""

import numpy as np
import pandas as pd


def main():
    N = 10
    df = pd.DataFrame({
           'A': pd.date_range(start='20190320',periods=N,freq='D'),
           'x': np.linspace(0,stop=N-1,num=N),
           'y': np.random.rand(N),
           'C': np.random.choice(['Low','Medium','High'],N).tolist(),
           'D': np.random.normal(100, 10, size=(N)).tolist()
        })
    print(df)
    print("=="*32)

    # reindex 重建索引
    print(df.reindex(index=[0,2,5], columns=['A','x']))
    print("=="*32)

    # reindex_like
    df1 = pd.DataFrame(np.random.randn(10,3), columns=['col1','col2','col3'])
    df2 = pd.DataFrame(np.random.randn(7,4), columns=['col1','col2','col3','col4'])

    print(df1)
    df1 = df1.reindex_like(df2)
    print(df1)
    print("=="*32)

    ###############################
    """
    填充时重新加注
        reindex()采用可选参数方法，它是一个填充方法，其值如下：
            pad/ffill - 向前填充值
            bfill/backfill - 向后填充值
            nearest  - 从最近的索引值填充
    """
    df1 = pd.DataFrame(np.random.randn(6,3), columns=['col1','col2','col3'])
    df2 = pd.DataFrame(np.random.randn(2,4), columns=['col1','col2','col3','col4'])
    print(df2.reindex_like(df1))
    print(df2.reindex_like(df1,method='ffill'))
    print("=="*32)
    # 填充限制，仅仅填充一行
    print(df2.reindex_like(df1,method='ffill',limit=1))
    print(df2.reindex_like(df1,method='backfill'))
    #print(df2.reindex_like(df1,method='nearest'))
    print("=="*32)


    ###############################################
    # rename()方法允许基于一些映射(字典或者系列)或任意函数来重新标记一个轴
    # rename()方法提供了一个inplace命名参数，默认为False并复制底层数据。 指定传递inplace = True则表示将数据重命名，直接修改原数据
    print(df2.rename(columns={'col1':'c1'}, index={1:'apple'}))
    print(df2)
    print("=="*32)
    df2.rename(columns={'col1':'c1'}, index={1:'apple'}, inplace=True)
    print(df2)












if __name__ == '__main__':
    main()
