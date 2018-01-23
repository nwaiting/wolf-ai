#coding=utf-8

"""
已知有1,2,5,9,10 这几种银币
求总数30最少几个银币
"""
def min_coin(n):
    if n < len(base_arr):
        return base_arr[n-1]

    min_num = n
    for i in xrange(1,n+1):
        if i < len(base_arr):
            min_num = min(min_num, base_arr[i-1] + min_coin(n - i - 1))
        else:
            base_arr.append(min_coin(i))
    return min_num

"""
1:d(1-1)+1
2:min(d(2-1)+1,d(2-2)+1)
3:min(d(3-1)+1,d(3-2)+1,d(3-3)+1)
4:min(d(4-1)+1),d(4-2)+1,d(4-3)+1,d(4-4)+1)
"""
def min_coin2(n):
    arr = [i for i in xrange(n+1)]
    for i in xrange(1, n+1):
        for j in xrange(len(base_arr)):
            if i >= base_arr[j]:
                arr[i] = min(arr[i], arr[i - base_arr[j]] + 1)
            else:
                break
    return arr

if __name__ == '__main__':
    base_arr = [1,2,5,10]
    sum_num = 18
    #print min_coin(sum_num)

    b = min_coin2(sum_num)
    print b
    print b[sum_num]
