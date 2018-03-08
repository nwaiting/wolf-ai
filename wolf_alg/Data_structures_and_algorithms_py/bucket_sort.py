#coding=utf-8

def bucket_sort(l):
    max_value = 0
    for i in l:
        if i > max_value:
            max_value = i
    arr = [0 for i in xrange(max_value+1)]
    for i in l:
        arr[i] += 1

    res = []
    for i in xrange(max_value+1):
        for j in xrange(0,arr[i]):
            res.append(i)
    return res

"""
合适大数据量的桶排序
"""
def select_sort(l):
    if len(l) <= 0:
        return l

    for i in xrange(len(l)-1):
        min_index = i
        for j in xrange(i+1, len(l)):
            if l[j] <= l[min_index]:
                min_index = j
        if min_index != i:
            l[min_index],l[i] = l[i],l[min_index]
    return l

def bucket_sort_bg(l):
    arr = [[] for i in xrange(10)]
    for i in l:
        arr[i/10].append(i)
        select_sort(arr[i/10])

    res = []
    for i in arr:
        res += i
    return res

if __name__ == '__main__':
    data = [20,5,2,18,21,5,3,4,8]
    #print bucket_sort(data)
    print bucket_sort_bg(data)
