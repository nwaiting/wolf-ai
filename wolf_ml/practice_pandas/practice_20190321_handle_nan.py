#coding=utf-8


"""
    常用操作有：
        检查缺失值
        缺少数据的计算
        清理/填充缺少数据
            df.fillna(0)  使用0进行填充
            pad/fill 填充方法向前
            bfill/backfill  填充方法向后

        丢失缺少的值
        替换丢失(或)通用值
"""


import numpy as np
import pandas as pd



def main():
    df = pd.DataFrame(np.random.randn(5, 3), index=['a', 'c', 'e', 'f',
        'h'],columns=['one', 'two', 'three'])
    df = df.reindex(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
    print(df)
    print("=="*32)

    # Pandas提供了isnull()和notnull()函数
    print(df['one'].isnull())   #返回bool值
    print("=="*32)

    print(df['one'].notnull())
    print("=="*32)

    # 在求和数据时，NA将被视为0，如果数据全部是NA，那么结果将是NA
    print(df['one'].sum())
    print("=="*32)

    # nan值填充
    # Pandas提供了各种方法来清除缺失的值。fillna()函数可以通过几种方法用非空数据“填充”NA值
    # 用0替换NaN
    print(df.fillna(0))
    print("=="*32)

    print(df.fillna(method='pad'))
    print("=="*32)

    # 丢失缺少的值
    # 如果只想排除缺少的值，则使用dropna函数和axis参数。 默认情况下，axis = 0，即在行上应用，这意味着如果行内的任何值是NA，那么整个行被排除
    df['two']['g'] = 0.188888888
    print(df)
    print("=="*32)
    print(df.dropna())
    print("=="*32)

    print(df)
    print(df.dropna(axis=1))
    print(df)
    print("=="*32)

    # 替换丢失(或)通用值
    # 很多时候，必须用一些具体的值取代一个通用的值。可以通过应用替换方法来实现这一点。用标量值替换NA是fillna()函数的等效行为
    df['two']['g'] = 1111
    df['two']['b'] = 2222
    df['two']['d'] = 2222
    print(df)
    print(df.replace({2222:0.2,1111:0.1}))








if __name__ == '__main__':
    main()
