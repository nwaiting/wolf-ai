#coding=utf-8

def count_sort(l):
    max_value = 0
    for i in l:
        if i > max_value:
            max_value = i
    arr = [0 for i in xrange(max_value+1)]
    for i in l:
        arr[i] += 1
    res = []
    for i in xrange(max_value+1):
        for j in xrange(arr[i]):
            res.append(i)
    return res

if __name__ == '__main__':
    data = [21,21,22,25,5,3,2,4,8,1]
    print count_sort(data)
