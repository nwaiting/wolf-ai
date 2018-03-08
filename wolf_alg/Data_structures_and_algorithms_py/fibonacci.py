#coding=utf-8

"""
基础数组算法
"""
def fibonacci_arr(n):
    arr = [i for i in xrange(n+1)]
    for i in xrange(2, n+1):
        arr[i] = arr[i-1] + arr[i-2]
    return arr[n]

"""
数组是最常用的数据结构之一，现在我们对数组的下标进行特殊处理，使每一次操作仅保留若干有用信息，新的元素不断循环刷新，
看上去数组的空间被滚动地利用，此模型我们称其为滚动数组。其主要达到压缩存储的作用
滚动数组的dp算法
"""
def fibonacci_arr_dp(n):
    arr = [i for i in xrange(3)]
    for i in xrange(2,n+1):
        arr[i%3] = arr[(i-1)%3] + arr[(i-2)%3]
    return arr[n%3]

"""
recursion
"""
def fibonacci(n):
    if n <= 1:
        if n==0:
            return 0
        else:
            return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

if __name__ == '__main__':
    from time import time
    calc_times = 35
    begin = time()
    print fibonacci(calc_times)
    first_time = time()
    print "first cost ", first_time-begin
    print fibonacci_arr_dp(calc_times)
    second_time = time()
    print "second time ", second_time - first_time
    print fibonacci_arr(calc_times)
    print "third time ", time() - second_time
