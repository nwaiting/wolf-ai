#coding=utf-8

"""
并查集:
并查集是一种树型的数据结构，用于处理一些不相交集合（Disjoint Sets）的合并及查询问题
"""

class edge(object):
    def __init__(self, start=None, end=None):
        self.start = start
        self.end = end

class GraphManager(object):
    def __init__(self, edge_num=3):
        if edge_num:
            self.parents = [-1 for i in xrange(edge_num)]
            self.edges = []
            self.edges.append(edge(0,1))
            self.edges.append(edge(1,2))
            self.edges.append(edge(0,2))

    def find(self, index):
        if index == self.parents[index] or -1 == self.parents[index]:
            return index
        return self.find(self.parents[index])

    def check(self):
        for item in self.edges:
            i_r = self.find(item.start)
            j_r = self.find(item.end)
            if i_r == j_r:
                return True
            self.union(i_r, j_r)

    def union(self, i, j):
        i_res = self.find(i)
        j_res = self.find(j)
        if i_res != j_res:
            self.parents[i_res] = j_res


class UnionFindSets(object):
    def __init__(self, arr=None):
        self.parents = arr

    def is_cycle(self):
        for i in xrange(len(self.parents)):
            res, flag = self.find(i)
            if i == res and flag:
                return True
            elif i > 0:
                self.union(i, i-1)
            print i, self.parents
        return False

    def find(self, index):
        tmp_index = index
        while True:
            tmp_value = self.parents[tmp_index]
            if tmp_value >= len(self.parents):
                return -1, False

            if -1 == self.parents[tmp_index]:
                return tmp_index, False

            if index == self.parents[tmp_index]:
                return index, True

            tmp_index = self.parents[tmp_index]

    def union(self, start=None, end=None):
        if start is None or end is None:
            return
        res1, flag1 = self.find(start)
        res2, flag2 = self.find(end)
        if res1 != res2:
            self.parents[res1] = res2

if __name__ == '__main__':
    run = 1
    if run == 1:
        record_pre = [-1 for i in xrange(10)]
        record_pre[1] = 2
        record_pre[7] = 8
        record_pre[8] = 9
        record_pre[9] = 7
        dis_sets = UnionFindSets(arr=record_pre)
        if dis_sets.is_cycle():
            print "have cycle"
        else:
            print "have no cycle"
    elif run == 2:
        gmanager = GraphManager()
        if gmanager.check():
            print "check success"
