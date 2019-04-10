#coding=utf-8


"""
    日期功能扩展了时间序列，在财务数据分析中起主要作用。在处理日期数据的同时，我们经常会遇到以下情况
        生成日期序列
        将日期序列转换为不同的频率
        常用函数：
            date_range  自然日
            bdate_range 工作日

    时间差(Timedelta)是时间上的差异，以不同的单位来表示。例如：日，小时，分钟，秒。它们可以是正值，也可以是负值。可以使用各种参数创建Timedelta对象
        pd.Timedelta
"""

import numpy as np
import pandas as pd



def main():
    #创建日期范围
    ds = pd.date_range('20190321', periods=10)
    print(ds)
    print("="*64)

    #更改日期频率
    print(pd.date_range('20190321', periods=10, freq='M'))
    print("="*64)

    # bdate_range() 函数
    # bdate_range()用来表示商业日期范围，不同于date_range()，它不包括星期六和星期天
    print(pd.bdate_range('20190321', periods=10))
    print("="*64)

    start = pd.datetime(2017, 11, 1)
    print(start)
    print("="*64)

def main2():
    print(pd.Timedelta('2 days 2 hours 15 minutes 30 seconds'))
    print("="*64)

    #整数
    print(pd.Timedelta(6, unit='h'))
    print("="*64)

    #数据偏移
    print(pd.Timedelta(days=2))
    print("="*64)

    # 运算操作
    s = pd.Series(pd.date_range('2012-1-1', periods=3, freq='D'))
    td = pd.Series([ pd.Timedelta(days=i) for i in range(3) ])
    df = pd.DataFrame(dict(A = s, B = td))
    print(df)
    print("="*64)

    #相加操作
    df['C'] = df['A'] + df['B']
    print(df)
    print("="*64)

    #相减操作
    df['D'] = df['C']-df['B']
    print(df)
    print("="*64)































if __name__ == '__main__':
    #main()
    main2()
