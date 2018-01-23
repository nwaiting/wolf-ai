#coding=utf-8

"""
C=10，三个宝石的体积为5，4，3，对应的价值为20，10，12。
状态d(i,j)表示前i个宝石装到剩余体积为j的背包里能达到的最大价值
状态转移：
    如果装入，在面对前2个宝石时， 背包就只剩下体积7来装它们，而相应的要加上2号宝石的价值12， d(3, 10)=d(2, 10-3)+12=d(2, 7)+12；
    如果不装入，体积仍为10，价值自然不变了， d(3, 10)=d(2, 10)。
"""
def get_bag_dp(wei, pi, con):
    length = len(wei)
    arr = [[0 for row in xrange(con+1)] for clo in xrange(length+1)]
    for i in xrange(1, length+1):
        for j in xrange(0, con+1):
            arr[i][j] = arr[i-1][j]
            if j >= wei[i-1]:
                arr[i][j] = max(arr[i][j], arr[i-1][j-wei[i-1]] + pieces[i-1])
    return arr

"""
使用滚动数组对dp算法进行空间优化
"""
def get_bag_dp2(wei, pi, con):
    length = len(wei)
    arr = [0 for row in xrange(con+1)]
    for i in xrange(length):
        for j in xrange(con, wei[i]-1, -1):
            print arr, con,j - wei[i],pi[i]
            arr[j] = max(arr[j], arr[j - wei[i]] + pi[i])
    return arr

if __name__ == '__main__':
    c = 20
    weights = [2,3,4,5,6]
    pieces = [6,3,6,4,5]
    # fun1
    b = get_bag_dp(weights, pieces, c)
    print b
    print b[len(weights)][c]

    # fun2
    b = get_bag_dp2(weights, pieces, c)
    print b
    print b[c]
