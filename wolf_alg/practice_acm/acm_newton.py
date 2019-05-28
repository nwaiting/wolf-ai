#coding=utf-8

import time

# binary search
def sqart_1(n):
    min_v = 0
    max_v = n
    mid = (max_v+min_v)/2
    delta = 0.000001
    mid_2 = mid*mid
    counter = 0
    while abs(mid_2 - n) > delta:
        if mid_2 > n:
            max_v = mid
        if mid_2 < n:
            min_v = mid
        mid = (max_v+min_v)/2
        mid_2 = mid*mid
        counter += 1
    print("total count={}".format(counter))
    return mid


def sqart_2(n):
    x = 1.0
    delta = 0.000001
    counter = 0
    while abs(x*x - n) > delta:
        x = (x + n/x)/2
        counter += 1
    print("total counter={}".format(counter))
    return x




if __name__ == '__main__':
    print(sqart_1(10))
    print(sqart_2(10))
