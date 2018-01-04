# -*- coding: utf-8 -*-
import sys
from consts import SIZE

def terrainCollision(hero,bound,terrain): #[0不碰-1左碰1右碰,0不碰-1上碰1下碰]
    l,r,u,d = bound
    result = [0,0]
    if l < 0 or r >= len(terrain[0]) or u < 0 or d >= len(terrain):
        return result

    if hero.vx < 0: px = hero.x-hero.width/2
    else: px = hero.x+hero.width/2
    if hero.vy < 0: py = hero.y-hero.height/2
    else: py = hero.y+hero.height/2

    if not hero.vy:
        for i in range(u,d-hero.land+1):
            if hero.vx < 0 and terrain[i][l]:
                result[0] = -1
                break
            elif hero.vx > 0 and terrain[i][r]:
                result[0] = 1
                break
    elif hero.vx < 0:
        lx = (l+1)*SIZE
        lyu = lyd = 0
        for i in range(u,d-hero.land+1):
            if terrain[i][l] and not terrain[i][l+1]:
                if not lyu: lyu = (i)*SIZE
                lyd = (i+1)*SIZE
        if lyd and lineCollision((px,hero.y-hero.height/2),
                                 (px,hero.y+hero.height/2),
                                 (hero.vx,hero.vy),(lx,lyu),(lx,lyd)):
            result[0] = -1
    elif hero.vx > 0:
        rx = r*SIZE
        ryu = ryd = 0
        for i in range(u,d-hero.land+1):
            if terrain[i][r] and not terrain[i][r-1]:
                if not ryu: ryu = (i)*SIZE
                ryd = (i+1)*SIZE
        if ryd and lineCollision((px,hero.y-hero.height/2),
                                 (px,hero.y+hero.height/2),
                                 (hero.vx,hero.vy),(rx,ryu),(rx,ryd)):
            result[0] = 1

    if hero.vy < 0 and not hero.vx:
        for j in range(l,r+1):
            if terrain[u][j]:
                result[1] = -1
                break
    elif hero.vy < 0:
        uy = (u+1)*SIZE
        uxl = uxr = 0
        for j in range(l,r+1):
            if terrain[u][j] and not terrain[u+1][j]:
                if not uxl: uxl = (j)*SIZE
                uxr = (j+1)*SIZE
        if uxr and lineCollision((hero.x-hero.width/2,py),
                                 (hero.x+hero.width/2,py),
                                 (hero.vx,hero.vy),(uxl,uy),(uxr,uy)):
            result[1] = -1
    elif hero.vy > 0:
        dy = d*SIZE
        dxl = dxr = 0
        for j in range(int(l),int(r+1)):
            if terrain[int(d)][j] and not terrain[int(d)-1][j]:
                if not dxl: dxl = (j)*SIZE
                dxr = (j+1)*SIZE
        if dxr and lineCollision((hero.x-hero.width/2,py),
                                 (hero.x+hero.width/2,py),
                                 (hero.vx,hero.vy),(dxl,dy),(dxr,dy)):
            result[1] = 1

    return result

def enemyCollision(hero,enemy): #返回值：0没有碰撞，1竖直碰撞，-1水平碰撞
    if not rectCollision(hero,enemy): return 0
    elif hero.y-hero.vy+hero.height/2 < enemy.y-enemy.height*0.1: return 1
    return -1

def rectCollision(s1,s2):
    if s1.x+s1.width/2 > s2.x-s2.width/2 and \
       s1.x-s1.width/2 < s2.x+s2.width/2 and \
       s1.y+s1.height/2 > s2.y-s2.height/2 and \
       s1.y-s1.height/2 < s2.y+s2.height/2:
        return True
    return False

def lineCollision(q1,q2,v,p1,p2):
    l1 = determineLinearEquation(q1,(q1[0]-v[0],q1[1]-v[1]))
    l2 = determineLinearEquation(q2,(q2[0]-v[0],q2[1]-v[1]))
    if not (l1 and l2): return False
    if f(l1,p1)*f(l1,p2) < 0 or f(l2,p1)*f(l2,p2) < 0 or \
       f(l1,p1)*f(l2,p1) < 0 or f(l1,p2)*f(l2,p2) < 0:
        return True
    return False

def determineLinearEquation(p1, p2):
    x1, y1, x2, y2 = p1[0], p1[1], p2[0], p2[1]
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

def f(coe, point):
    return coe[0]*point[0] + coe[1]*point[1] + coe[2]
