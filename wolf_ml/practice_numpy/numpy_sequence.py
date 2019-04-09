#coding=utf-8

"""
    # 等差数列
    print(np.linspace(0.1, 1, 10, endpoint=True))
    print(np.arange(0.1, 1.1, 0.1))
    总结：
        arange 侧重点在于增量，不管产生多少个数
        linspace 侧重于num, 即要产生多少个元素，不在乎增量

    # 等比数列
    numpy.logspace(start, stop, num=50, endpoint=True, base=10.0, dtype=None, axis=0)
    np.logspace(1, 4, 4, endpoint=True, base=2) # 2**1---2**4

"""


import numpy as np

def main():
    # 等差数列
    print(np.linspace(0.1,1,5))

    print(np.arange(0.1, 1.0, 0.2))

    #等比数列

    print(np.logspace(1,4,4,base=2))








if __name__ == '__main__':
    main()
