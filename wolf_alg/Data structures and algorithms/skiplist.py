#coding=utf-8

import random
"""
跳表数据结构，
参考 https://github.com/google/leveldb/blob/master/db/skiplist.h
"""
KMaxHeight = 12

class KeyNode(object):
    def __init__(self, k, n=None):
        self.key_ = k
        self.next_ = k

class SkipList(object):
    def __init__(self):
        self.max_height_ = 1
        self.heads_ = [KeyNode(None) for i in xrange(KMaxHeight)]

    def Insert(self, tkey):
        prev = [None for i in xrange(KMaxHeight)]
        tnode = self.FindGreaterOrEqual(tkey, prev)
        if tnode and tnode.key_ == tkey:
            print "find key ", tkey
            return None
        height = self.RandomHeight()
        if height > self.max_height_:
            for i in xrange(self.max_height_, height):
                prev[i] = self.heads_[i]
            self.max_height_ = height
        knode = KeyNode(tkey)
        for i in xrange(height):
            knode.next_ = prev[i].next_
            prev[i].next_ = knode

    def FindGreaterOrEqual(self, tkey, tres):
        import time
        level = self.max_height_ - 1
        while True:
            """
            此处需要优化 下一层开始位置应该为上一层当前的开始位置 
            """
            thead = self.heads_[level]
            nextnode = thead.next_
            while nextnode and nextnode.key_ < tkey:
                thead = nextnode
                nextnode = nextnode.next_
            if tres:
                tres[level] = thead
            if level == 0:
                return nextnode
            else:
                level -= 1
        return None

    def Equal(self, tkey):
        r = self.FindGreaterOrEqual(tkey,None)
        if r and r.key_ == tkey:
            return True
        return False

    def RandomHeight(self):
        kbranching = 4
        height = 1
        while height < KMaxHeight and random.randint(0,3) == 0:
            height += 1
        return height

if __name__ == '__main__':
    #print random.randint(0,1)
    #print random.randint(0,1)
    #print random.randint(0,1)
    sl = SkipList()
    sl.Insert('this')
    sl.Insert('is')
    sl.Insert('test')
    sl.Insert('怎么样')
    print sl.Equal('is')
    print sl.Equal('test')
    print sl.Equal('yes')
    print sl.Equal('怎么样')
