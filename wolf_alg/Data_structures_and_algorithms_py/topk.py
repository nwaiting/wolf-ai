#coding=utf-8

"""
堆排序分为两步：
1、调整并创建k堆
2、循环将第一个和第i个互换，然后对前i-1个进行堆调整，最后结果即为排序好的堆数据
"""

def heap_build(l):
    for i in xrange(len(l)/2-1,-1,-1):
        adjust(l,i, len(l)-1)

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
    heap_build(l)
    for i in xrange(len(l)-1, 0, -1):
        if i == 1 and l[i] > l[0]:
            break
        l[0],l[i] = l[i],l[0]
        adjust(l, 0, i-1)
    return l

if __name__ == '__main__':
    data = [1,5,55,25,15,35,75]
    print heap_sort(data)
    print data
