#coding=utf-8

'''
@parameter
    st: start search
'''
def bfs(st):
    tmp = [st,]
    flags = [0 for i in xrange(len(double_list) + 1)]
    flags[st] = 1
    while len(tmp) > 0:
        i = tmp[0]
        tmp.pop(0)
        print i
        for j in xrange(1, len(double_list) + 1):
            if flags[j] <= 0 and double_list[i-1][j-1] > 0:
                tmp.append(j)
                flags[j] = 1

if __name__ == '__main__':
    double_list = [[0, 1, 1, 0, 0],
            [0, 0, 1, 1, 0],
            [0, 1, 1, 1, 0],
            [1, 0, 0, 0, 0],
            [0, 0, 1, 1, 0]]
    bfs(0)
