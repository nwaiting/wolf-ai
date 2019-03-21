#coding=utf-8


"""
    当任何匹配特定值的数据(NaN/缺失值，尽管可以选择任何值)被省略时，稀疏对象被“压缩”。 一个特殊的SparseIndex对象跟踪数据被“稀疏”的地方。 这将在一个例子中更有意义。 所有的标准Pandas数据结构都应用了to_sparse方法
"""

import numpy as np
import pandas as pd


def main():
    ts = pd.Series(np.random.randn(10))
    ts[2:-2] = np.nan

    print(ts)
    print('='*64)

    tst = ts.to_sparse()
    print(tst)
    print('='*64)

    print(tst.density)
    print('='*64)

    # 将稀疏对象转换成标准密集形式
    print(tst.to_dense())
    print('='*64)

    # 稀疏Dtypes
    # 稀疏数据应该具有与其密集表示相同的dtype。 目前支持float64，int64和booldtypes。 取决于原始的dtype，fill_value默认值的更改
    















if __name__ == '__main__':
    main()
