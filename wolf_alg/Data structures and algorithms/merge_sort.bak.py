#!/usr/bin/env python
# coding: utf-8

"""
@file: merge_sort.bak.py
@time: 2017/1/18 15:04
"""


def merge(left, right):
    result = list()
    l, r = 0, 0
    while l < len(left) and r < len(right):
        if left[l] <= right[r]:
            result.append(left[l])
            l += 1
        else:
            result.append(right[r])
            r += 1
    if l < len(left):
        result += left[l:]
    if r < len(right):
        result += right[r:]
    return result


def merge_sort(data_list):
    if len(data_list) <= 1:
        return data_list

    middle = len(data_list)/2
    left = merge_sort(data_list[:middle])
    right = merge_sort(data_list[middle:])
    return merge(left, right)


if __name__ == "__main__":
    data_list = [249, 23794, 234, 23, 576, 789, 34, 10, 39457, 4345]
    print merge_sort(data_list)
