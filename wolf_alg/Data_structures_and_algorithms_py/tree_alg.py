#coding=utf-8

import os
import sys

"""
    heap
"""

def heap_build(l):
    for i in range(int(len(l)/2)-1,-1,-1):
        adjust(l, i, len(l)-1)

def adjust(l, begin, end):
    while True:
        root = begin * 2 + 1
        if root >= end:
            break
        if root + 1 <= end and l[root] < l[root+1]:
            root += 1
        if l[root] < l[begin]:
            break
        l[root],l[begin]=l[begin],l[root]
        begin = root

def heap_sort(l):
    #创建heap
    heap_build(l)

    #adjust heap
    for i in range(len(l)-1, 0, -1):
        if i == 1 and l[i] > l[0]:
            break
        l[0],l[i] = l[i],l[0]
        adjust(l, 0, i-1)
    return l

def main():
    data = [234,5,234,5670,23,1231,235,678,100]
    print(heap_sort(data))


if __name__ == '__main__':
    main()
