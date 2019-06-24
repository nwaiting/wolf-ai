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
        print (summ)
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
            #print (data_list[i - 1][j], data_list[i][j], data_list[i][j + 1])
    print (data_list[0][0])

"""
    第二种方法是真的是由O(n)的空间完成，当然也是利用动态规划思想，但是正如上面的方法思路，如果从上到下计算最小值，
        那么无论如何最后都需要计算一遍最小值，但是如果换个角度想，从最后一行向上到第一行，那么最后求出的值就一个，而无需再求最小值
    令dp[j]表示从最后一行到达当前行的第j列的最小值，那么有dp[j] = triangle[i][j] + min(dp[j], dp[j+1])
    另外有一个好处是，由于后一行始终比当前行的元素多，所以j+1不存在越界的问题

"""
def max_route2(data_list):
    if len(data_list)<=0:
        return 0
    dp = data_list[-1][:]
    for i in range(len(data_list)-2,-1,-1):
        print("======================")
        for j in range(len(data_list[i])-1):
            dp[j] = data_list[i][j] + max(dp[j], dp[j+1]) #需要理解这个状态转移方程
            print(dp)
    return dp[0]

if __name__ == "__main__":
    # data_list = [1, -1, 5, -10, 13, 2, -5, 17]
    # print max_continue_list(data_list)
    data_list_second = [[9, 0, 0, 0, 0],
                        [12, 15, 0, 0, 0],
                        [10, 6, 8, 0, 0],
                        [2, 18, 9, 5, 0],
                        [19, 7, 10, 4, 16]]
    #print (max_route(data_list_second))
    print(max_route2(data_list_second))
