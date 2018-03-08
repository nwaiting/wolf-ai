#coding=utf-8
"""
简单hash算法
"""
class MyHash(object):
    def __init__(self, tseed):
        self.seed_ = (tseed & 0X7FFFFFFF)
        if self.seed_ == 0:
            self.seed_ = 1

    def Next(self):
        #seed_ = (seed_ * A) % M,    where M = 2^31-1
        m = 2147483647 #2^31-1
        a = 16807   #bits 14, 8, 7, 5, 2, 1, 0
        p = self.seed_ * a
        self.seed_ = (p >> 31) + (p & m)
        if self.seed_ > m:
            self.seed_ -= m
        return self.seed_


if __name__ == '__main__':
    t = 0xdeadbeef
    mhash = MyHash(t)
    print mhash.Next()
    print mhash.Next()
    print mhash.Next()
    print mhash.Next()
