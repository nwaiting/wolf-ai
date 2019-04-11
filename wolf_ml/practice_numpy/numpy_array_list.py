#coding=utf-8

"""
    numpy.ndarray和list如何相互转换？
"""

import numpy as np

def f1():
    # list 转 numpy
    a = [1,2,3]
    aa = np.array(a)
    print(aa)
    print(type(aa))

    # numpy 转 list
    b = np.arange(1,10)
    print(b)
    print(type(b))
    bb = b.tolist()
    print(bb)
    print(type(bb))


def f2():
    pass


if __name__ == '__main__':
    f1()
    f2()
