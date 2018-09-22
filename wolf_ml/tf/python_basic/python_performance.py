#coding=utf-8

"""
python的性能优化
1、改进算法，选择合适的数据结构
    O(1) -> O(lg n) -> O(n lg n) -> O(n^2) -> O(n^3) -> O(n^k) -> O(k^n) -> O(n!)
    字典 (dictionary) 与列表 (list)：
        Python 字典中使用了 hash table，因此查找操作的复杂度为 O(1)，而 list 实际是个数组
    集合 (set) 与列表 (list)：
        set 的 union， intersection，difference 操作要比 list 的迭代要快
    对循环的优化：
        有多重循环的尽量将内层的计算提到上一层
    充分利用 Lazy if-evaluation 的特性：
        python 中条件表达式是 lazy evaluation 的，也就是说如果存在条件表达式 if x and y，在 x 为 false 的情况下 y 表达式的值将不再计算
    字符串的优化：
        在字符串连接的使用尽量使用 join() 而不是 +
        当对字符串可以使用正则表达式或者内置函数来处理的时候，选择内置函数
        对字符进行格式化比直接串联读取要快
    使用列表解析（list comprehension）和生成器表达式（generator expression）：
        使用列表解析：
        for i in range (1000000):
            a = [w for w in list]
    交换变量：
        交换两个变量的值使用 a,b=b,a 而不是借助中间变量 t=a;a=b;b=t;
    在循环的时候使用 xrange 而不是 range；使用 xrange 可以节省大量的系统内存，因为 xrange() 在序列中每次调用只产生一个整数元素。而 range() 將直接返回完整的元素列表，用于循环时会有不必要的开销。在 python3 中 xrange 不再存在，里面 range 提供一个可以遍历任意长度的范围的 iterator。
    使用局部变量，避免"global" 关键字。python 访问局部变量会比全局变量要快得多，因	此可以利用这一特性提升性能。
    if done is not None 比语句 if done != None 更快，读者可以自行验证；
    在耗时较多的循环中，可以把函数的调用改为内联的方式；
    使用级联比较 "x < y < z" 而不是 "x < y and y < z"；
    while 1 要比 while True 更快（当然后者的可读性更好）；
    build in 函数通常较快，add(a,b) 要优于 a+b。

"""

def func1():
    """
    对代码优化的前提是需要了解性能瓶颈在什么地方，程序运行的主要时间是消耗在哪里，对于比较复杂的代码可以借助一些工具来定位，python 内置了丰富的性能分析工具，
    如 profile,cProfile 与 hotshot 等。其中 Profiler 是 python 自带的一组程序，能够描述程序运行时候的性能，并提供各种统计帮助用户定位程序的性能瓶颈。Python 标准模块提供三种 profilers:cProfile,profile 以及 hotshot。
    profile 的使用非常简单，只需要在使用之前进行 import 即可。具体实例如下：
    清单 8. 使用 profile 进行性能分析
    import profile
    def profileTest():
       Total =1;
       for i in range(10):
           Total=Total*(i+1)
           print Total
       return Total
    if __name__ == "__main__":
       profile.run("profileTest()")
    """
    pass

if __name__ == '__main__':
    func1()
