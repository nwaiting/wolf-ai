# -*- coding: utf-8 -*-
from point import Point
from element import Poly
from geometry import *

def CPCollision(c,g):
    m = Point(c.x,c.y) #球心
    #粗略判断，如果点不在拓展多边形内，直接返回False
    if not checkPointPoly(m,g.epoly):
        return False
    #已知点在拓展多边形内，下面逐个检查点是否在拓展线段内
    p = g.poly #图形g的多边形
    n = Point(c.x-c.vx,c.y-c.vy) #上一个时刻的球心
    v = determineLinearEquation(m,n) #速度直线
    for i in range(p.n):
        p1,p2 = p.endpoints[i],p.endpoints[i+1]
        l = p.lines[i]
        if checkPointSegment(l,p1,p2,c.r,m):
            #已知点在拓展线段内，下面检查球的运动轨迹是否与线段相交
            mm = getMovePoint(m,getPerpendicularVector(l,p.centerPoint),c.r)
            nm = getMovePoint(mm,(-c.vx,-c.vy))
            if checkSegmentSegment(determineLinearEquation(mm,nm),mm,nm,l,p1,p2):
                #已知碰撞到了这条线段，下面改变球的速度
                unit = (l[0]**2+l[1]**2)**0.5
                cos = l[0]/unit
                sin = l[1]/unit
                c.vn = c.vx*cos+c.vy*sin
                c.vp = -c.vx*sin+c.vy*cos
                c.vn = -c.vn
                c.vx = c.vn*cos-c.vp*sin
                c.vy = c.vn*sin+c.vp*cos
                return True
            #否则碰撞到了这条线段的端点，但是我们不管它，放到下面讨论
    #球没有碰到某一线段，下面检查球是否包含了某一角
    for q in p.vertices:
        if m-q < c.r:
            #已知球碰到了这一点，下面改变球的速度
            #解方程组，计算球碰撞的角度：（t是一个比例，无用）
            #      A    B    t
            #~   | r    0    vx  q.x-c.x|
            #A = | 0    r    vy  q.y-c.y|
            #    |r*vx r*vy  0    v*proj|
            _v = (c.vx**2+c.vy**2)*0.5 #速度的模
            proj = (c.r**2-getDistanceSquare(v,q))**0.5 #半径在速度方向上的投影
            A,B,t = solveEquationSet([[c.r,0,c.vx,q.x-c.x],
                                      [0,c.r,c.vy,q.y-c.y],
                                      [c.vx*c.r,c.vy*c.r,0,_v*proj]])
            unit = (A**2+B**2)**0.5
            #print unit #unit应该接近于1
            cos = A/unit
            sin = B/unit
            c.vn = c.vx*cos+c.vy*sin
            c.vp = -c.vx*sin+c.vy*cos
            c.vn = -c.vn
            c.vx = c.vn*cos-c.vp*sin
            c.vy = c.vn*sin+c.vp*cos
            return True
        
    #最后什么都没碰到，其实球可能已经跑到里面了
    return False
