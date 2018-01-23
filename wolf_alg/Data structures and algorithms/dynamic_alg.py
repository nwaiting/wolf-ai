#!/usr/bin/env python
# coding: utf-8

"""
@file: dynamic_alg.py
@time: 2017/1/18 17:45
"""

"""
{-1, 2, 5, -10, 4, 9}
求最大子序列和
"""
def max_continue_list(data_list):
    summ, maxm = 0, 0
    for i in data_list:
        summ += i
        print summ
        if summ > maxm:
            maxm = summ
        if summ < 0:
            summ = 0
    return maxm

"""
            9
          12  15
        10  6  8
       2  18  9   5
     19 7  10  4   16
     求最大路径和
"""
def max_route(data_list):
    for i in range(len(data_list) - 1, 0, -1):
        for j in range(i):
            data_list[i - 1][j] += data_list[i][j] if data_list[i][j] > data_list[i][j + 1] else data_list[i][j + 1]
            print data_list[i - 1][j], data_list[i][j], data_list[i][j + 1]
    print data_list[0][0]


if __name__ == "__main__":
    # data_list = [1, -1, 5, -10, 13, 2, -5, 17]
    # print max_continue_list(data_list)

    data_list_second = [[9, 0, 0, 0, 0],
                        [12, 15, 0, 0, 0],
                        [10, 6, 8, 0, 0],
                        [2, 18, 9, 5, 0],
                        [19, 7, 10, 4, 16]]
    print max_route(data_list_second)
