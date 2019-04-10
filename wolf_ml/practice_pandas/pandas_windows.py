#coding=utf-8


"""
    为了处理数字数据，Pandas提供了几个变体，如滚动，展开和指数移动窗口统计的权重。 其中包括总和，均值，中位数，方差，协方差，相关性等
    常用函数：
        .rolling()函数
            这个函数可以应用于一系列数据。指定window=n参数并在其上应用适当的统计函数
        .expanding()函数
        .ewm()函数
"""

import numpy as np
import pandas as pd


def main():
    df = pd.DataFrame(np.random.randn(10,4),index=np.linspace(1,10,10),columns=['col1','col2','col3','col4'])
    print(df)
    print("=="*32)

    # rolling函数
    # 注 - 由于窗口大小为3(window)，前两个元素有空值，第三个元素的值将是n，n-1和n-2元素的平均值。这样也可以应用上面提到的各种函数了
    # 应用：滚动窗口计算 按指定周期计算，如2周期求和
    print(df.rolling(window=3).mean())
    print("=="*32)

    # .expanding()函数
    # 这个函数可以应用于一系列数据。 指定min_periods = n参数并在其上应用适当的统计函数
    # 用途：提供扩展转换。累计计算，如累加求和
    print(df.expanding(min_periods=3).mean())
    print("=="*32)

    df1 = pd.DataFrame({ "date": pd.date_range("2018-12-04", periods=7),
        "income": [1000, 2000, np.nan, 3000, 4000, 5000, 6000]})
    print(df1)
    print(df1.expanding(min_periods=2,axis=0)['income'].sum())
    print("=="*32)

    # .ewm()函数 指数加权滑动（ewm）, 指数加权滑动平均（ewma）
    # ewm()可应用于系列数据。指定com，span，halflife参数，并在其上应用适当的统计函数。它以指数形式分配权重。
    print(df.ewm(com=0.5).mean())
    print("=="*32)





if __name__ == '__main__':
    main()
