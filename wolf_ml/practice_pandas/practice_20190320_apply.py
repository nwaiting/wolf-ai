#coding=utf-8

"""
    pipe() 表合理函数应用
    apply() 行或列函数应用
    applymap() 元素函数应用
"""


import numpy as np
import pandas as pd


def main():
    dates = pd.date_range("20190320", periods=6)
    df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=['col1','col2','col3', 'col4'])
    print(df)
    print('=='*32)

    # 为DataFrame中的所有元素相加一个值2
    def adder(a,b):
        return a+b
    #操作之后，原来的df没有改变，知识新生成了一个df
    print(df.pipe(adder, 2))
    print(df)
    print('=='*32)

    ############################################
    # 可以使用apply()方法沿DataFrame或Panel的轴应用任意函数，它与描述性统计方法一样，采用可选的axis参数。 默认情况下，操作按列执行，将每列列为数组。
    print(df.apply(np.mean, axis=0))
    print(df.apply(np.mean, axis=1))
    print(df.apply(lambda x:x.max()-x.min()))
    print('=='*32)


    ##############################################
    # 并不是所有的函数都可以向量化(也不是返回另一个数组的NumPy数组，也不是任何值)，在DataFrame上的方法applymap()和类似于在Series上的map()接受任何Python函数，并且返回单个值
    print(df.loc[:,'col1'].map(lambda x:x*100))
    print('=='*32)

    print(df.applymap(lambda x:x*100))
    print('=='*32)


def main2():
    pass


if __name__ == '__main__':
    main()
