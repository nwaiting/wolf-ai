#coding=utf-8
"""
多路归并
原始数据
0	5	11	18
4	7	9	14
6	8	12	17
10	13	15	16
1	2	3
结果列表：

第一步：
5	11	18
4	7	9	14
6	8	12	17
10	13	15	16
1	2	3
结果列表：0

第二步：
5	11	18
4	7	9	14
6	8	12	17
10	13	15	16
2	3
结果列表：0 1

应用：适用于将多个排序好的文件进行归并后合并成大文件
    合并后直接写入新的文件中，每次加载老的文件不需要全部加载到内存中，可以节约内存
"""
import time

def multi_merge(l):
    if len(l) <= 0:
        return None
    arr_index = [0 for row in xrange(len(l))]
    res = []
    flag = 0
    while flag < len(l):
        flag = 0
        min_value = 99999
        min_value_index = -1
        for i in xrange(len(l)):
            if arr_index[i] < len(l[i]):
                if l[i][arr_index[i]] < min_value:
                    min_value_index = i
                    min_value = l[i][arr_index[i]]
            else:
                flag += 1
        res.append(min_value)
        arr_index[min_value_index] += 1
    return res

if __name__ == '__main__':
    arr = [[1,5,8,20],[3,4,7,8,9],[1,25,34,56,78],[23,56,99]]
    print multi_merge(arr)
