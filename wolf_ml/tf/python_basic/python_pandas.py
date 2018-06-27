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

def func2():
    pf_data = pd.read_csv(file, header=None, nrows=None, usecols=[5,7])
    pf_data = pf_data.dropna() #删除掉空行
    #print(pf_data.head())
    #print(pf_data[5].head())
    #print(pf_data[7].values)

    #groupby_user = pf_data.groupby([5]).count()
    #groupby_user = pf_data.groupby([5]).size()
    #groupby_user = pf_data.groupby([5])
    #for k,v in groupby_user:
    #    print(k, v.count()[7])

if __name__ == '__main__':
    func1()
