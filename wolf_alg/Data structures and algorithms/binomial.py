#coding=utf-8

"""
使用dp
求解c(n,k) = c(n-1,k) + c(n-1,k-1)
"""
def binomial(n, k):
    arr =[[0 for raw in xrange(k+1)] for clo in xrange(n+1)]
    for i in xrange(n+1):
        arr[i][1] = 1
    for i in xrange(1,n+1):
        for j in xrange(1,k+1):
            if j == 1 or i == j:
                arr[i][j] = 1
            else:
                arr[i][j] = arr[i-1][j] + arr[i-1][j-1]
    return arr[n][k]

if __name__ == '__main__':
    print binomial(9, 5)
