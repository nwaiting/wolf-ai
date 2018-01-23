#coding=utf-8

def binary_search(l, v):
    if len(l) <= 0:
        return None
    begin = 0
    end = len(l)
    middle = (end + begin)/2
    while begin <= end:
        middle = (end + begin)/2
        print "times ", middle
        if l[middle] == v:
            return middle
        elif v < l[middle]:
            end = middle - 1
        else:
            begin = middle + 1

def binary_search_recursion(l, begin, end, v):
    if begin > end:
        return None

    middle = (begin + end) / 2
    if v == l[middle]:
        return middle
    elif v > l[middle]:
        return binary_search_recursion(l, middle + 1, end, v)
    else:
        return binary_search_recursion(l, begin, middle - 1, v)

if __name__ == '__main__':
    l = [100, 130, 180, 200, 253, 362, 458, 596, 687, 785, 852, 934]
    print binary_search(l, 362)
    print binary_search_recursion(l, 0, len(l), 362)
