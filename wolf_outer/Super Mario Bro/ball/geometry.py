# -*- coding: utf-8 -*-
#函数库
#用于计算点、线段、射线、直线之间的各种关系
#以及确定上、代入直线方程、计算行列式等基础运算

from point import Point
from functools import wraps
import sys

#检查点是否在多边形内
def checkPointPoly(point,poly):
    flag = True
    centerPoint = poly.centerPoint
    lines = poly.lines
    for line in lines:
        product = f(line, point) * f(line, centerPoint)
        if product < 0:
            flag = False #在多边形外
    return flag

#检查点是否在一条线段向两边伸展R形成的矩形内
def checkPointSegment(l,p1,p2,r,q):
    dC = r*(l[0]**2+l[1]**2)**0.5
    l1 = (l[0],l[1],l[2]-dC)
    l2 = (l[0],l[1],l[2]+dC)
    if checkSign(f(l1,q),f(l2,q)):
        return False
    return True

#计算凸多边形某边的垂直向心方向
def getPerpendicularVector(l,c):
    if f(l,c) > 0:
        return (l[0],l[1])
    return (-l[0],-l[1])

#计算某点朝某一方向移动一段距离得到的点
def getMovePoint(p,v,d=0):
    if d: #输入了距离，按距离移动
        m = (v[0]**2+v[1]**2)**0.5
        return Point(p.x+v[0]/m*d,p.y+v[1]/m*d)
    return Point(p.x+v[0],p.y+v[1])

#检查两条线段是否相交
def checkSegmentSegment(l1,p1,q1,l2,p2,q2):
    if checkSign(f(l1,p2),f(l1,q2)) or checkSign(f(l2,p1),f(l2,q1)):
        return False
    return True

#确定直线方程
def determineLinearEquation(p1, p2):
    x1, y1, x2, y2 = p1.x, p1.y, p2.x, p2.y
    if x1 == x2:
        if y1 == y2:
            sys.stderr.write("Error: determineLinearEquation(p1, p2) gets two same points: (%s, %s).\n"\
                             %(x1, y1))
            return None
        A, B = 1, 0
    else:
        A, B = y1-y2, x2-x1
    C = -A*x1-B*y1
    return (A,B,C)

#代入直线方程
def f(coe, point):
    return coe[0]*point.x + coe[1]*point.y + coe[2]

#解直线交点
def getIntersection(l1, l2):
    D = float(l1[0]*l2[1] - l2[0]*l1[1])
    if D == 0:
        sys.stderr.write("Error: getIntersection(l1, l2) gets two same line: %sx + %sy = %s"\
                         %l1)
        return None
    Dx = l1[1]*l2[2] - l2[1]*l1[2]
    Dy = l1[2]*l2[0] - l2[2]*l1[0]
    return Point(Dx/D, Dy/D)

#计算点到直线距离平方
def getDistanceSquare(l,p):
    return f(l,p)**2/(l[0]**2+l[1]**2)

#计算行列式
#|p1.x p1.y 1|
#|p2.x p2.y 1|
#|p3.x p3.y 1|
def calculateDeterminant(p1, p2, p3):
    return p1.x*(p2.y-p3.y) - p1.y*(p2.x-p3.x) + p2.x*p3.y - p3.x*p2.y

#计算一般行列式
def determinant(D):
    n = len(D)
    if n == 1: return D[0][0]
    return sum((-1)**i*D[0][i]*determinant([r[:i]+r[i+1:] for r in D[1:]]) \
               for i in range(n))

#克莱姆法则求解线性非齐次方程组
def solveEquationSet(A):
    D = [r[:-1] for r in A]
    _D = determinant(D)
    if _D == 0:
        sys.stderr.write("Error: The equation set has no solutions")
        return
    solutions = []
    for i in range(len(A)):
        for j in range(len(A)):
            D[j][i] = A[j][-1]
        _Dx = determinant(D)
        solutions.append(float(_Dx)/_D)
        for j in range(len(A)):
            D[j][i] = A[j][i]
    return solutions

#判断是否同号或为零
def checkSign(n1,n2):
    if n1 >= 0 and n2 >= 0 or n1 <= 0 and n2 <= 0:
        return True
    return False
