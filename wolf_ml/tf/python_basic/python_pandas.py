#coding=utf-8

import pandas as pd

def func1():
    dates = pd.date_range(pd.to_datetime('2018-06-06'), pd.to_datetime('2018-12-31'), freq='M')
    print(dates)

    with open('a.csv', 'a') as fout:
        with open('b.csv') as f:
            f.next() #跳过csv的header，跳过头部的column name信息
            for line in f.readlines:
                fout.write(line)

if __name__ == '__main__':
    func1()
