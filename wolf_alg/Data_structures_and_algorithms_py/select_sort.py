#coding=utf-8

def select_sort(l):
    for i in xrange(len(l)-1):
        min_index = i
        for j in xrange(i+1, len(l)):
            if l[j] < l[min_index]:
                min_index = j
        if min_index != i:
            l[min_index],l[i] = l[i],l[min_index]
    return l

if __name__ == '__main__':
    data = [1,21,13,5,10,20,2,3,5]
    print select_sort(data)
