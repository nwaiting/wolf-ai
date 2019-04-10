#coding=utf-8



"""
    警告和疑难意味着一个看不见的问题。在使用Pandas过程中，需要特别注意的地方
    与Pandas一起使用If/Truth语句当尝试将某些东西转换成布尔值时，Pandas遵循了一个错误的惯例。 这种情况发生在使用布尔运算的。 目前还不清楚结果是什么。
    如果它是真的，因为它不是zerolength？ 错误，因为有错误的值？ 目前还不清楚，Pandas提出了一个ValueError
"""


import numpy as np
import pandas as pd


def main():
    # 提示ValueError异常，因为在if条件，它不清楚如何处理它。错误提示是否使用None或任何这些
    #if pd.Series([False, True, False]):
    #    print("yes")

    if pd.Series([False, True, False]).any():
        print("any")
    print("=="*32)

    # 要在布尔上下文中评估单元素Pandas对象，请使用方法.bool()
    print(pd.Series([True]).bool())
    print("=="*32)

    # 按位布尔值
    # 按位布尔运算符(如==和!=)将返回一个布尔系列，这几乎总是需要的
    s = pd.Series(range(5))
    print(s==4) #返回一个Series
    print("=="*32)

    # isin
    s = pd.Series(list('abc'))
    print(s.isin(['a','d',1]))
    print("=="*32)

    # 重构索引与ix陷阱
    df = pd.DataFrame(np.random.randn(6, 4), columns=['one', 'two', 'three','four'],index=list('abcdef'))
    print(df)

    # df.ix和df.reindex在这种操作下等价，在后面的操作中不等价
    print(df.ix[['b', 'c', 'e']])
    print(df.reindex(['b','c','e']))
    print("=="*32)

    # 重要的是要记住，reindex只是严格的标签索引。这可能会导致一些潜在的令人惊讶的结果，例如索引包含整数和字符串的病态情况。
    print(df.ix[[1,2,4]])
    print(df.reindex([1,2,4]))
    print("=="*32)











if __name__ == '__main__':
    main()
