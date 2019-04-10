#coding=utf-8


"""
    Pandas I/O API是一套像pd.read_csv()一样返回Pandas对象的顶级读取器函数
    读取文本文件(或平面文件)的两个主要功能是read_csv()和read_table()，它们都使用相同的解析代码来智能地将表格数据转换为DataFrame对象
"""


import numpy as np
import pandas as pd


def main():
    df = pd.read_csv("a.csv")
    print(df)
    print('='*64)

    #自定义索引
    df = pd.read_csv('a.csv', index_col=['S.No'])
    print(df)
    print('='*64)

    df = pd.read_csv('a.csv', index_col=['City'])
    print(df)
    print('='*64)

    # 转换器 dtype的列可以作为字典传递，转换数据类型
    print(df.dtypes)
    df = pd.read_csv('a.csv', dtype={'Salary':np.float64})
    print(df.dtypes)
    print(df)
    print('='*64)

    #指定标题名称 使用names参数指定标题的名称
    df = pd.read_csv('a.csv', names=['a', 'b', 'c','d','e'])
    print(df)
    print('='*64)

    # 指定标题名称，使用names参数指定标题的名称，header参数删除原标题
    df = pd.read_csv('a.csv', names=['a', 'b', 'c','d','e'], header=0)
    print(df)
    print('='*64)

    # skiprows跳过指定的行数，
    df = pd.read_csv('a.csv')
    print(df)
    print('='*64)
    df = pd.read_csv('a.csv', skiprows=2)   # 跳过开始两行
    print(df)
    print('='*64)
    df = pd.read_csv('a.csv', skiprows=1)   #跳过开始1行
    print(df)
    df = pd.read_csv('a.csv', skiprows=0)
    print(df)
    print('='*64)


















if __name__ == '__main__':
    main()
