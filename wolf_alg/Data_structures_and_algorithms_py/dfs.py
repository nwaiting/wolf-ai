#coding=utf-8

def dfs(row):
    stack_list.append(row)
    print stack_list
    for clon in xrange(len(dl[row])):
        if dl[row][clon] > 0 and clon not in stack_list: #顶点是否已经在当前路径中
            dfs(clon)
            stack_list.pop()

if __name__ == '__main__':
    dl = [
    [0, 1, 1, 0, 0, 0],
    [1, 0, 0, 1, 1, 0],
    [1, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0]]
    stack_list = list()
    dfs(0)
