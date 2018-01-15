#coding=utf-8

def func1():
    from distutils.core import setup, Extension
    pass


def func2():
    from decimal import Decimal
    a = 5.23459734957345979
    print(a)
    print('%.2f'%a)
    print(Decimal(a).quantize(Decimal('0.00')))

if __name__ == '__main__':
    #func1()
    func2()
