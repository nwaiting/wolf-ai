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

def func4():
    """
    os.stat()
        获取文件属性
    """
    import os
    statinfo = os.stat(os.path.abspath(__file__))
    print(statinfo.st_size)
    #当前文件的字节数

    print(dir(statinfo))
    #'count', 'index', 'n_fields', 'n_sequence_fields', 'n_unnamed_fields', 'st_atime', 'st_atime_ns', 'st_ctime', 'st_ctime_ns', 'st_dev', 'st_file_attributes', 'st_gid', 'st_ino', 'st_mode', 'st_mtime', 'st_mtime_ns', 'st_nlink', 'st_size', 'st_uid'

def func5():
    """
    下划线在python中的作用，有时候是为了省略，有时候不关心内部格式时，可以直接输出
    """
    data = {'a':1, 'b':2}
    for _ in data.items():
        print(_)

def func6():
    """
    list的extend()
    extend()：即为两个list相加
    """
    aList = [123, 'xyz', 'zara', 'abc', 123]
    bList = [2009, 'manni']

    #方法1
    aList_copy = aList[:]
    aList_copy += bList
    print(aList_copy)

    #方法2
    print(aList + bList)

    #方法3
    aList.extend(bList)
    print(aList)

def func7():
    """
    判断字符串是否只由空格组成
    """
    str = "       "
    print(str.isspace())    # 结果为True

    str = "This is string example....wow!!!";
    print(str.isspace())    #结果为False

def func8(_):
    """
    locals() 函数会以字典类型返回当前位置的全部局部变量
    """
    data1 = [1,2,3]
    data2 = 1
    print(locals())  #结果 {'data2': 1, 'data1': [1, 2, 3], '_': 1}

def func9():
    """
    sys.stdout.write和print的区别
    sys.stdout.write('\r')  当只有换行时，一直在一样显示
    """
    import sys
    import time
    for _ in range(10):
        time.sleep(0.5)
        print('hello')

    #
    for _ in range(10):
        time.sleep(0.5)
        sys.stdout.write('hello {}\r'.format(_))

if __name__ == '__main__':
    #func1()
    #func2()
    #func3()
    #func4()
    #func5()
    #func6()
    #func7()
    #func8(1)
    func9()
