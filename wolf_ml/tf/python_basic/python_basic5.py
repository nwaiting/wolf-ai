#coding=utf-8

def func1():
    """
    set的使用功能
    """
    a = set()
    a.add('a')
    a.add('b')
    print(a)

    #set转list
    print(list(a))

    #list转set
    b = ['a','b','a']
    print(set(b))

    #set求并集
    c = {'a','b','c'}
    print(a|c)

    #这种方法只能使用if不能使用else
    d = [1 for i in c if i in a]
    #生成集合
    d = {1 for i in c if i in a}
    #生成字典
    d = {i:i for i in c if i in a}
    print(d)

    #使用if和else 都可以使用
    d = [1 if i in a else 0 for i in c]
    print(d)

def func2():
    """
    math的功能使用
    """
    import math
    print(math.pow(2, 4))  #2^4
    print(math.sqrt(5))

if __name__ == '__main__':
    #func1()
    func2()
