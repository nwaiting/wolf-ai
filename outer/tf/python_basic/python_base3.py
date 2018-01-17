#coding=utf-8

def func1():
    from distutils.core import setup, Extension
    pass


def func2():
    """
    控制小数位的输出
    """
    from decimal import Decimal
    a = 52348.23459734957345979
    b = 1.111111111111
    print(a)
    print('%.2f'%a)
    print(Decimal(a).quantize(Decimal('0.00')))

    #精度控制
    print('{0:.3f}'.format(a,b))
    #其中.2表示长度为2的精度，f表示float类型
    print('{:.2f}'.format(321.33345))
    #控制宽度
    print('{0:4}{1:3}'.format('abc', 'python'))

if __name__ == '__main__':
    #func1()
    func2()
