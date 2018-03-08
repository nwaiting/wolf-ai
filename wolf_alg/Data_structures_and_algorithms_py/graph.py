#coding=utf-8

def dfs(index):
    """
    先遍历顶点 然后对每个顶点进行深度遍历
    """
    dfs_list.append(index)
    for colu in xrange(len(datas[index])):
        if datas[index][colu] > 0 and colu not in dfs_list:
            dfs(colu)
            show(dfs_list)
            dfs_list.pop()

def dfswithlist(index):
    """
    先深度遍历一个顶点
    """
    dfs_list.append(index)
    for colu in front_array[index]:
        if colu not in dfs_list:
            dfswithlist(colu)
            show(dfs_list)
            dfs_list.pop()

def bfs(index):
    """
    首先遍历首个顶点 然后对每个顶点的邻接点开始遍历
    """
    start_list = [index,]
    flags = [index,]
    while len(start_list) > 0:
        show(start_list)
        start_v = start_list[0]
        start_list.pop(0)
        for j in xrange(len(datas[start_v])):
            if datas[start_v][j] > 0 and j not in flags:
                start_list.append(j)
                flags.append(j)

def bfswithlist(index):
    """
    先遍历顶点的邻接顶点
    """
    start_list = [index,]
    flags = [index,]
    while len(start_list) > 0:
        start_v = start_list[0]
        start_list.pop(0)
        show(flags)
        for colu in front_array[start_v]:
            if colu not in flags:
                flags.append(colu)
                start_list.append(colu)


def show(l):
    for i in l:
        print indexs[i],
    print ""

if __name__ == '__main__':
    """
    邻接矩阵
    适合边数比较丰富的图结构中
    """
    indexs = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H',8:'I'}
    datas = [[0,1,0,0,0,1,0,0,0],
    [1,0,1,0,0,0,0,0,1],
    [0,1,0,1,0,0,0,0,1],
    [0,0,1,0,1,0,1,1,1],
    [0,0,0,1,0,1,0,1,0],
    [1,0,0,0,1,0,1,0,0],
    [0,0,0,1,0,1,0,1,0],
    [0,0,0,1,1,0,1,0,0],
    [0,1,1,1,0,0,0,0,0]]
    print "dfs#############################"
    dfs_list = list()
    #dfs(0)
    print "bfs#############################"
    bfs(0)

    """
    邻接表
    适合边数较少的结构中
    """
    front_array = []
    front_array.append([1,5])
    front_array.append([0,2,8])
    front_array.append([1,3,8])
    front_array.append([2,4,6,7,8])
    front_array.append([3,5,7])
    front_array.append([0,4,6])
    front_array.append([3,5,7])
    front_array.append([3,4,6])
    front_array.append([1,2,3])
    print "dfs with list###########################"
    dfs_list = list()
    #dfswithlist(0)
    print "bfs with list###########################"
    bfswithlist(0)
