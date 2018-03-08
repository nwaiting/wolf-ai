#coding=utf-8

def insert_sort(l):
    for i in xrange(1, len(l)):
        for j in xrange(i-1, -1, -1):
            if l[j] > l[j+1]:
                l[j],l[j+1]=l[j+1],l[j]
    return l

if __name__ == '__main__':
    data = [1,20,40,28,18,2,3,5]
    print insert_sort(data)
