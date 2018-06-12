#coding=utf-8

import numpy as np

def func1():
    #多元正太分布
    np.random.multivariate_normal()
    #狄利克雷分布
    np.random.dirichlet()
    #伽马分布
    np.random.gamma()
    #logistic分布
    np.random.logistic()

    #从x中根据概率p，抽取出一个y大小的矩阵
    np.random.choice(x, y, p=None)

def func2():
    a = np.array([[1,2,3],[4,5,6]])
    #对所有元素全部相加
    print(a.sum())
    #对每一列相加，保留列数
    print(a.sum(axis=0))
    print(a.sum(axis=0).reshape(3,1))
    #对每一行相加，保留行数
    print(a.sum(axis=1))
    print(a.sum(axis=1).reshape(2,1))
    #取行,列数据
    print(a[0,:])

    b = np.random.choice([0,1,2,3,4], 10, [0.1,0.1,0.8])
    print(b)

def func3():
    a = [1,2,3,4,5]
    c = [0,1,2,3,4]
    b = [2,3,4,5,6]
    d = np.array(c)[np.where(np.array(a)==3)]
    print(d)
    print(np.array(c)/np.array(b)) #直接用对应的数据进行除法计算
    print(np.array(a)/np.array(b))
    print((np.array(c)/np.array(b)) * (np.array(a)/np.array(b)))




    
if __name__ == '__main__':
    #func2()
    func3()
