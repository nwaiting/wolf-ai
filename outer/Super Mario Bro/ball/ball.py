# -*- coding: utf-8 -*-
import tkinter as tk
from time import sleep,clock
from random import randrange, random, randint
from point import Point
from element import Poly
from geometry import *
from CPCollision import *
import gc, sys, winsound, threading

INTERVAL = 0.01
D = 6
SIZE = 60
R = 12
V = 7
WIDTH = 480
HEIGHT = 600
PICTURE = "./ball/"

#������
class Sprite:
    def __init__(self,_id,x,y,w,h):
        self.children = []
        self.parent = None
        self.x, self.y = x, y
        self.id = _id
        self.type = canvas.type(_id)
        self.width = w
        self.height = h
    def move(self):
        if not self.parent:
            self.ax, self.ay = self.x, self.y
        for child in self.children:
            child.ax, child.ay = child.x+self.ax, child.y+self.ay
            child.move()
        if self.id:
            if self.type == "image":
                if hasattr(self,"seq"):
                    for img in self.seq:
                        canvas.coords(img,self.ax,self.ay)
                else: canvas.coords(self.id,self.ax,self.ay)
            elif self.type == "text":
                canvas.coords(self.id,self.ax,self.ay)
            elif self.type == "polygon":
                print(canvas.coords(self.id))
            else:
                canvas.coords(self.id,
                              self.ax-self.width/2.0,self.ay-self.height/2.0,
                              self.ax+self.width/2.0,self.ay+self.height/2.0)
    def addChild(self,child):
        self.children.append(child)
        child.parent = self
    def removeChild(self,child):
        for i in range(len(child.children)):
            child.removeChild(child.children[0])
        self.children.remove(child)
        canvas.delete(child.id)
        child.parent = None

class Block(Sprite):
    def __init__(self,x,y,n):
        self.num = n
        self.shrink = 0

        color = self.getColor()
        dark = color[:]
        darker = color[:]
        for i in range(3):
            dark[i] -= dark[i]/8
            darker[i] /= 3
        Sprite.__init__(self,
                        canvas.create_rectangle(0,0,0,0,outline=toColor(darker),
                                                fill=toColor(dark)),
                        x,y,SIZE,SIZE)
        self.addChild(Sprite(canvas.create_rectangle(0,0,0,0,outline="",
                                                     fill=toColor(color)),
                             1,1,SIZE*0.8,SIZE*0.8))
        self.addChild(Sprite(canvas.create_text(x,y,font=("Cooper Black",
                                                          24),
                                                fill=toColor(darker),
                                                text=str(n),anchor="center"),
                             0,0,0,0))
    def hitted(self):
        self.num -= 1
        if self.num == 0:
            for key in sortedBlocks:
                sortedBlocks[key].remove(self)
            stage.removeChild(self)
            return
        canvas.itemconfig(self.children[1].id,text=str(self.num))
        self.width = self.height = SIZE
        self.shrink = 1
    def update(self):
        if self.shrink == 1:
            self.width -= 2
            self.height -= 2
            if self.width == SIZE-8:
                self.shrink = -1
        elif self.shrink == -1:
            self.width += 2
            self.height += 2
            if self.width == SIZE:
                self.shrink = 0
        self.children[0].width = self.width*0.8
        self.children[0].height = self.height*0.8
    def getColor(self):
        base = [0,255,randint(0,255)]
        color = []
        for i in range(3):
            index = randint(0,3-i-1)
            color.append(base[index])
            del base[index]
        return color
    def setPoly(self): #������������չ���ɵĶ�����
        self.poly = Poly([Point(self.x-SIZE/2,self.y-SIZE/2),
                          Point(self.x+SIZE/2,self.y-SIZE/2),
                          Point(self.x+SIZE/2,self.y+SIZE/2),
                          Point(self.x-SIZE/2,self.y+SIZE/2)])
        self.epoly = Poly([Point(self.x-SIZE/2-R,self.y-SIZE/2-R),
                           Point(self.x+SIZE/2+R,self.y-SIZE/2-R),
                           Point(self.x+SIZE/2+R,self.y+SIZE/2+R),
                           Point(self.x-SIZE/2-R,self.y+SIZE/2+R)])

class Ball(Sprite):
    def __init__(self,x,y,vx,vy,color):
        self.vx,self.vy = vx,vy
        self.vn,self.vp = 0,0
        self.r = R
        self.run = True
        Sprite.__init__(self,
                        canvas.create_oval(0,0,0,0,fill=toColor(color)),
                        x,y,R*2,R*2)
        bright = color[:]
        for i in range(3):
            bright[i] += (255-bright[i])/2
        self.addChild(Sprite(
            canvas.create_oval(0,0,0,0,outline="",fill=toColor(bright)),
            R*0.4,-R*0.4,6,6))
    def update(self):
        if not self.run: return
        self.x += self.vx
        self.y += self.vy
        if self.x+self.r > WIDTH:
            self.vx = -abs(self.vx)
        elif self.x-self.r < 0:
            self.vx = abs(self.vx)
        if self.y-self.r < 0:
            self.vy = abs(self.vy)

#�¼�������
class MouseHandler:
    def __init__(self):
        self.run = False
    def onClick(self,e):
        global accel
        if self.run:
            self.run = False
            self.click = (e.x,e.y)
        else:
            accel = True

def winClose():
    global closed
    closed = True
    root.destroy()

def close():
    global canvas,listener,stage,blocks,speed,color,cur,pic,sortedBlocks
    canvas.forget()
    del canvas,listener,stage,blocks,speed,color,cur,pic,sortedBlocks
    gc.collect()

def main(_root):
    global root,canvas,closed,paused,accel,listener,stage,blocks,speed,color,cur,pic
    root = _root
    root.geometry("%dx%d" %(WIDTH,HEIGHT))
    canvas = tk.Canvas(root,width=WIDTH,height=HEIGHT)
    canvas.pack()
    closed = False
    paused = False
    accel = False
    root.protocol("WM_DELETE_WINDOW",winClose)
    listener = MouseHandler()
    canvas.bind_all("<Button-1>", listener.onClick)
    stage = Sprite(0,0,0,WIDTH,HEIGHT)
    pic = tk.PhotoImage(file=PICTURE+"background0.gif")
    stage.addChild(Sprite(canvas.create_image(0,0,
                                              image=pic,anchor="nw"),
                          0,0,WIDTH,HEIGHT))
    level = 30
    emitPos = (WIDTH/2,HEIGHT-R) #������λ��
    blocks = []
    ball = None

    speed = randrange(2)*40-20
    base = [0,255,randint(1,254)]
    color = []
    for i in range(3):
        index = randint(0,3-i-1)
        color.append(base[index])
        if color[-1] != 0 and color[-1] != 255:
            cur = i
        del base[index]

    while True:
        startGame(level)
        accel = False
        if closed: return
        for block in blocks:
            if block.y >= HEIGHT-SIZE:
                canvas.create_text(WIDTH/2,HEIGHT/2,
                                   text="GAME OVER\n%3d LEVELS" %(level-1),
                                   font=("Cooper Black",48),anchor="center")
                if wait(2,canvas.update): return
                close()
                return 1
        if ball: stage.removeChild(ball)
        emitPos,ball = loop(emitPos,level)
        if closed: return
        level += 1

def startGame(level):
    #���ӷ���
    for i in range(int(WIDTH/SIZE)):
        if random() < 0.4 or not blocks and i == WIDTH/SIZE-1:
            block = Block(i*SIZE+SIZE/2,-SIZE/2,level+1)
            blocks.append(block)
            stage.addChild(block)
    #�����ƶ�����
    for i in range(SIZE):
        sleep(INTERVAL)
        if closed: return
        for block in blocks:
            block.y += 1
        stage.move()
        canvas.update()
    for block in blocks:
        block.setPoly()
    #��ʼ���������¼���������listener.run����ΪFalse
    listener.run = True
    while True:
        sleep(INTERVAL)
        if closed or not listener.run: return
        canvas.update()

def loop(pos,level):
    global sortedBlocks,speed,color,cur
    num = level
    t = 0
    balls = []
    revBlocks = []
    y = blocks[0].y
    s = 0
    for i,block in enumerate(blocks):
        if block.y != y:
            y = block.y
            row = blocks[s:i]
            row.reverse()
            revBlocks += row
            s = i
    row = blocks[s:]
    row.reverse()
    revBlocks += row
    #�����������ַ�ʽ������ʹ���뷽������ײ���Ⱥ�����
    sortedBlocks = {(1,0):blocks,(0,1):blocks[::-1],
                    (0,0):revBlocks,(1,1):revBlocks[::-1]}
    #print sortedBlocks
    #���㷢���ٶ�
    click = listener.click
    d = ((click[0]-pos[0])**2+(click[1]-pos[1])**2)**0.5
    vx = (click[0]-pos[0])*V/d
    vy = (click[1]-pos[1])*V/d

    nextPos = None
    if False and level > 1:
        stage.removeChild(stage.children[1])

    clockTime = clock() #clockTime���ڼ�����������ʱ��
    frame = 0
    time = 0.0
    sys.stdout.write("fps:%7.2f\r" %(1/INTERVAL))
    while True:
        runTime = clock()
        frame += 1
        if accel: time += runTime-clockTime
        else: time += max(runTime-clockTime,INTERVAL)
        if frame == 30: #ÿ��30֡����һ��fps
            sys.stdout.write("fps:%7.2f\r" %(frame/time))
            frame = time = 0
        if not accel: sleep(max(INTERVAL-runTime+clockTime,0)) #��ȥ����sleep֮�侭����ʱ��
        clockTime = clock()

        if closed: return None,None
        if paused:
            canvas.update()
            continue

        #����
        if num > 0:
            t += 1
            if t == D:
                #��ɫ����
                if color[cur]+speed >= 255:
                    for i in range(3):
                        if color[i] == 255:
                            newCur = i
                            break
                    color[cur] = 255
                    cur = newCur
                    speed = -speed
                elif color[cur]+speed <= 0:
                    for i in range(3):
                        if color[i] == 0:
                            newCur = i
                            break
                    color[cur] = 0
                    cur = newCur
                    speed = -speed
                else: color[cur] += speed

                t = 0
                num -= 1
                ball = Ball(pos[0],pos[1],vx,vy,color)
                balls.append(ball)
                stage.addChild(ball)

        flag = False
        for ball in balls:
            x = y = None
            if ball.vx < 0: t0 = 0
            else: t0 = 1
            if ball.vy < 0: t1 = 0
            else: t1 = 1
            #���������ٶȷ�������������˳��
            for block in sortedBlocks[(t0,t1)]:
                if block.x == x or block.y == y:
                    continue #ͬ��ͬ��ֻ��ײһ��
                if CPCollision(ball,block):
                    block.hitted()
                    x,y = block.x,block.y

            ball.update()
            if ball.y+ball.r > HEIGHT:
                ball.y = HEIGHT-ball.r
                ball.run = False
                ball.vx = max(V/5.0,abs(ball.vx))
                if not nextPos: #�����´η���λ��
                    nextPos = (ball.x,ball.y)
                    landedBall = ball
            if ball.run or ball.x != nextPos[0]: flag = True
            if not ball.run:
                #���ƻ�ȥ
                if abs(ball.x-nextPos[0]) < abs(ball.vx):
                    ball.x = nextPos[0]
                    if ball.id < landedBall.id:
                        stage.removeChild(ball)
                        balls.remove(ball)
                    elif ball.id > landedBall.id:
                        stage.removeChild(landedBall)
                        balls.remove(landedBall)
                        landedBall = ball
                elif ball.x > nextPos[0]:
                    ball.x -= abs(ball.vx)
                else:
                    ball.x += abs(ball.vx)
        for block in blocks:
            block.update()

        stage.move()
        if not accel or frame%4 == 0: canvas.update()

        if balls and not flag:
            for ball in balls[:-1]:
                stage.removeChild(ball)
            balls[-1].x,balls[-1].y = nextPos
            return nextPos,balls[-1]

def toColor(color):
    return '#%06x'%sum(int(color[i])<<(i*8) for i in range(3))

def wait(t,func=None):
    for i in range(int(t/INTERVAL)):
        if closed:
            return True
        sleep(INTERVAL)
        if func: func()
    return False

if __name__ == '__main__':
    PICTURE = '.'+PICTURE
    main(tk.Tk())
