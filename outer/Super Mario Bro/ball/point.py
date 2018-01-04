# -*- coding: utf-8 -*-
#Point类，可以作为：
#1 普通用于计算的点
#2 多边形中包含时针、凹凸性等属性的点
#3 路径搜索算法中的节点
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.parent = self.poly = None
        self.clock = self.id = 0
        self.concave = self.skip = False

    def toTuple(self):
        return (self.x, self.y)
        
    #运算符重载
    #
    #p1==p2用于判断两点是否相同
    #此符号重载后保留字in和list的内置函数delete()也受影响
    def __eq__(self, p):
        if self.x == p.x and self.y == p.y:
            return True
        return False
    #p1!=p2与上面相反
    def __ne__(self, p):
        if p and self.x == p.x and self.y == p.y:
            return False
        return True

    #p1-p2用于计算两点间距离
    def __sub__(self, p):
        return ((self.x-p.x)**2 + (self.y-p.y)**2) ** 0.5
