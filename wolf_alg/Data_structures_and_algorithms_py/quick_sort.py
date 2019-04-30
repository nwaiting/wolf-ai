#!/usr/bin/env python
# coding: utf-8

"""
@file: quick_sort.py
@time: 2017/1/18 15:17
"""
import random


def qsort(d_list, left, right):
    if left >= right:
        return d_list
    key = d_list[left]
    l, r = left, right
    while l < r:
        while d_list[r] >= key and l < r:
            r -= 1
        while d_list[l] <= key and l < r:
            l += 1
        print (d_list, l, r, left, right)
        d_list[l], d_list[r] = d_list[r], d_list[l]
    d_list[left], d_list[l] = d_list[l], d_list[left]
    qsort(d_list, left, l - 1)
    qsort(d_list, l + 1, right)
    return d_list


def qsort_bark(data_list, left, right):
    if left >= right:
        return data_list
    key = data_list[left]
    lp, rp = left, right
    while lp <= rp:
        while lp <= rp and data_list[lp] <= key:
            lp += 1
        while lp <= rp and data_list[rp] > key:
            rp += 1
        data_list[lp], data_list[rp] = data_list[rp], data_list[lp]
    data_list[lp], data_list[left] = data_list[left], data_list[lp]
    qsort_bark(data_list, left, lp)
    qsort_bark(data_list, rp + 1, right)
    return data_list


def qsort_middle(data_list, left, right):
    if left >= right:
        return data_list
    key_index = int((right + left)/2)
    key = data_list[key_index]
    lp, rp = left, right
    while lp < rp:
        while rp > lp and data_list[lp] <= key:
            lp += 1
        while rp > lp and data_list[rp] >= key:
            rp -= 1
        print (data_list, lp, rp, left, right, key_index)
        data_list[lp], data_list[rp] = data_list[rp], data_list[lp]
    qsort_middle(data_list, left, key_index - 1)
    qsort_middle(data_list, key_index + 1, right)
    return data_list


def quick_sort(data_list):
    return qsort(data_list, 0, len(data_list) - 1)
    #return qsort_middle(data_list, 0, len(data_list) - 1)  error
    #return qsort_bark(data_list, 0, len(data_list) - 1)  error

#20180830
def quick_s(data, left, right):
    if left >= right:
        return data
    l = left
    r = right
    key = data[l]
    while l < r:
        #注：先从右边开始遍历寻找
        while data[r] >= key and l < r:
            r -= 1
        while data[l] <= key and l < r:
            l += 1
        data[l],data[r] = data[r],data[l]
    data[left],data[l] = data[l],data[left]
    quick_s(data, left, l-1)
    quick_s(data, l+1, right)
    return data

def quick_sort(d, l, r):
    if l >= r:
        return d

    random.seed(time.time())
    r_index = l
    #r_index = r
    key = d[r_index]
    tmp_l,tmp_r = l,r
    while tmp_l < tmp_r:
        #这里是先遍历右边还是先遍历左边和初始值选择有关，当初始值选择左边的元素，则先从右边开始遍历
        while tmp_l < tmp_r and d[tmp_l] <= key:
            tmp_l += 1
        while tmp_l < tmp_r and d[tmp_r] >= key:
            tmp_r -= 1
        d[tmp_l],d[tmp_r] = d[tmp_r],d[tmp_l]
        print("d=",d,tmp_l,tmp_r,r_index)
    d[tmp_r],d[r_index]=d[r_index],d[tmp_r]
    print("d==",d,tmp_l,tmp_r,r_index)
    quick_sort(d, l, tmp_l-1)
    quick_sort(d, tmp_l+1, r)
    return d

def quick_sort_random(d, l, r):
    if l >= r:
        return d

    random.seed(time.time())
    r_index = random.randint(l, r)
    key = d[r_index]
    tmp_l,tmp_r = l,r
    while tmp_l < tmp_r:
        while tmp_l < tmp_r and d[tmp_r] >= key:
            tmp_r -= 1
        while tmp_l < tmp_r and d[tmp_l] <= key:
            tmp_l += 1
        d[tmp_l],d[tmp_r] = d[tmp_r],d[tmp_l]
        print("d=",d,tmp_l,tmp_r,r_index)
    d[tmp_r],d[r_index]=d[r_index],d[tmp_r]
    print("d==",d,tmp_l,tmp_r,r_index)
    quick_sort_random(d, l, tmp_l-1)
    quick_sort_random(d, tmp_l+1, r)
    return d

if __name__ == "__main__":
    data_list = [44678, 2, 4676, 67868, 4546, 464, 8, 56, 67, 676]
    #print (quick_sort(data_list))
    print(quick_s(data_list, 0, len(data_list)-1))
