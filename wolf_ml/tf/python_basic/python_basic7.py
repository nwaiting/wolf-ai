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


if __name__ == '__main__':
    #func1()
    #func2()
    #func3()
    func4()
