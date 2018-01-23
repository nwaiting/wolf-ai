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

def func3():
    """
    线程设置：
        join:
            join() 代表主线程要等待子线程执行完再继续执行（被阻塞），期间是无法执行的
            用 Ctrl+C 试验可知，当使用了 join() 时，主线程不能及时接收到退出信号。要等子线程都执行完，才会处理退出信号
            所以使用join后，子线程不能及时处理Ctrl+C的信号
        setDaemon：
            setDaemon(True) 代表让子线程跟随主线程销毁
    信号：
        信号 SIGINT，代表 Ctrl+C 或 pm2 的 stop。信号 SIGTERM，代表 kill命令 或 pm2 的 kill
    """
    import threading,time,signal,sys

    def printa():
        while True:
            print('printa')
            time.sleep(1)
    def printb():
        while True:
            print('printb')
            time.sleep(1)
    def quit(signum,frame):
        print('program quit')
        sys.exit()

    #设置信号
    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)

    a = threading.Thread(target=printa)
    b = threading.Thread(target=printb)
    a.start()
    b.start()

    flag = 0
    if flag:
        a.join()
        b.join()
    else:
        a.setDaemon(True)
        b.setDaemon(True)

def func4():
    """
    if条件太长时：
        1、添加斜杠\
        2、使用括号
    """
    a = 1
    b = 2
    c = 3
    d = 4
    if a == 1 or \
        b == 2:
        print('test if')

    if (a == 1 or b == 2):
        print('test if 2')

def func5():
    #返回浮点数x的四舍五入值
    print(round(3.456789))
    print(round(3.456789, 1))
    print(round(3.456789, 2))
    print(round(3.456789, 3))

    import numpy as np
    print(np.array([1,2,3.5]))

    # set求差集
    a = {1,2,3,4,5,6}
    b = {1,3,5}
    c = a-b
    print(c)
    print(type(c), list(c))

def func6():
    import numpy as np
    """
        transpose就是改变高维数组的形状
    """
    # 一个数组中有2个元素，每个元素中有3个元素，每个元素中有5个元素
    array_a = np.array(range(30)).reshape(2,3,5)
    print(np.shape(array_a))
    array_b = np.transpose([array_a])
    print(np.shape(array_b))

def func7():
    import numpy as np
    """
        linspace 创建等差数列 在指定的间隔内返回均匀间隔的数字
    """
    print(np.linspace(1,10))

def func8():
    """
    实现tail -f 功能
    fileObject.seek(offset[, whence])
    参数：
        offset -- 开始的偏移量，也就是代表需要移动偏移的字节数
        whence：可选，默认值为 0。给offset参数一个定义，表示要从哪个位置开始偏移；0代表从文件开头开始算起，1代表从当前位置开始算起，2代表从文件末尾算起。
    """
    import time
    with open(filename, 'rb') as fd:
        fd.seek(0,2)
        while True:
            current_position = fd.tell()
            line = fd.readline()
            if line:
                print(line)
            else:
                fd.seek(curr_position)
            time.sleep(1)

if __name__ == '__main__':
    #func1()
    #func2()
    #func3()
    #func4()
    #func5()
    #func6()
    #func7()
    func8()
