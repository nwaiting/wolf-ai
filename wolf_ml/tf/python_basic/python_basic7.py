#coding=utf-8

def func1():
    """
    os.path.realpath 和 abspath区别：
        realpath 返回的是 使用软链 的真实地址，使用软连接的目标文件的真实地址
        abspath 返回目标地址
    """
    pass


def func2():
    """
    整数和浮点数除法：
        / 表示一定是浮点数除法
        // 表示整数除法

    """
    a = 3
    b = 8
    print(b/a)  #2.666666
    print(b//a) #2

    a = 3.0
    b = 8.0
    print(b/a)  #2.666666
    print(b//a) #2.0

def func3():
    """
    set()
    """
    ss = '你好不好不好啊'
    print(set(ss))


if __name__ == '__main__':
    #func1()

    #func2()

    func3()
