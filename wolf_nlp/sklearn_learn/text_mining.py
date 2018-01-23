#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from sklearn import datasets
import sys, os, subprocess, urllib, time, urllib2
import requests

from matplotlib import pyplot as plt
from matplotlib import animation
from numpy import *

def  main():
    f = open("MD5.txt","r")
    lines = f.readlines()
    for line in lines:
        filename = line.split('|')[0]
        url = "http://jump.synacast.com/80353b42d5b3a70ca3d35e6de67e2c69.mp4?type=media.proxy&rtype=redirect"
        print url
	res=None
        try:
            """
            print url
            req = urllib2.Request(url)
            req.get_method = lambda: 'HEAD'
            res = urllib2.urlopen(req)
            """
            res = requests.head(url=url)
        except urllib2.HTTPError as e:
            print "{0}".format(res)
            print "{0}".format(e)
        else:
            print "=======", res.request
            print res.headers
            print res.status_code
            print res.headers['Location']
            """
            rescode = res.getcode()
            if (rescode == 302):
                mp4url = res.headers['Location']
                print mp4url
                if (urllib.urlopen(mp4url).getcode == 200):
                    f1 = open('dest.txt','w')
                    f1.write(filename)
            """

def loadDataSet():
    """
    加载数据集

    :return:输入向量矩阵和输出向量
    """
    dataMat = []; labelMat = []
    fr = open('testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])]) #X0设为1.0，构成拓充后的输入向量
        labelMat.append(int(lineArr[2]))
    return dataMat,labelMat

def sigmoid(inX):
    return 1.0/(1+exp(-inX))

def gradAscent(dataMatIn, classLabels, history_weight):
    """
    逻辑斯谛回归梯度上升优化算法
    :param dataMatIn:输入X矩阵（100*3的矩阵，每一行代表一个实例，每列分别是X0 X1 X2）
    :param classLabels: 输出Y矩阵（类别标签组成的向量）
    :return:权值向量
    """
    dataMatrix = mat(dataMatIn)             #转换为 NumPy 矩阵数据类型
    labelMat = mat(classLabels).transpose() #转换为 NumPy 矩阵数据类型
    m,n = shape(dataMatrix)                 #矩阵大小
    alpha = 0.001                           #步长
    maxCycles = 500
    weights = ones((n,1))
    for k in range(maxCycles):              #最大迭代次数
        h = sigmoid(dataMatrix*weights)     #矩阵内积
        error = (labelMat - h)              #向量减法
        weights += alpha * dataMatrix.transpose() * error  #矩阵内积
        history_weight.append(copy(weights))
    return weights

def stocGradAscent1(dataMatrix, classLabels, numIter=150):
    """
    改进的随机梯度上升算法
    :param dataMatIn:输入X矩阵（100*3的矩阵，每一行代表一个实例，每列分别是X0 X1 X2）
    :param classLabels: 输出Y矩阵（类别标签组成的向量）
    :param numIter: 迭代次数
    :return:
    """
    dataMatrix = array(dataMatrix)
    m,n = shape(dataMatrix)
    weights = ones(n)                                           #初始化为单位矩阵
    for j in range(numIter):
        dataIndex = range(m)
        for i in range(m):
            alpha = 4/(1.0+j+i)+0.0001                          #步长递减，但是由于常数存在，所以不会变成0
            randIndex = int(random.uniform(0,len(dataIndex)))   #总算是随机了
            h = sigmoid(sum(dataMatrix[randIndex]*weights))
            error = classLabels[randIndex] - h
            weights = weights + alpha * error * dataMatrix[randIndex]
            del(dataIndex[randIndex])                           #删除这个样本，以后就不会选到了
    return weights

history_weight = []
dataMat,labelMat=loadDataSet()
gradAscent(dataMat, labelMat, history_weight)
fig = plt.figure()
currentAxis = plt.gca()
ax = fig.add_subplot(111)
line, = ax.plot([], [], 'b', lw=2)

def draw_line(weights):
    x = arange(-5.0, 5.0, 0.1)
    y = (-weights[0]-weights[1]*x)/weights[2]   #令w0*x0 + w1*x1 + w2*x2 = 0，其中x0=1，解出x1和x2的关系
    line.set_data(x, y)
    return line,

# initialization function: plot the background of each frame
def init():
    dataArr = array(dataMat)
    n = shape(dataArr)[0]
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    for i in range(n):
        if int(labelMat[i])== 1:
            xcord1.append(dataArr[i,1]); ycord1.append(dataArr[i,2])
        else:
            xcord2.append(dataArr[i,1]); ycord2.append(dataArr[i,2])
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')
    plt.xlabel('X1'); plt.ylabel('X2');

    return draw_line(zeros((n,1)))

# animation function.  this is called sequentially
def animate(i):
    return draw_line(history_weight[i])


def matrix():
    # call the animator.  blit=true means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(history_weight), interval=10, repeat=False,
                                   blit=True)
    plt.show()
    anim.save('gradAscent.gif', fps=2, writer='imagemagick')

d = [[0,5,3,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,1,3,6,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,8,7,6,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,6,8,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,3,5,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,3,3,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,8,4,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,2,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,3,3,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,3,5,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,5,2,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,6,6,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
"""
d=[[0,0,0,5,4,0,0],
   [0,0,0,8,7,0,0],
   [0,0,0,9,8,0,0],
   [0,0,0,0,0,9,10],
   [0,0,0,0,0,3,2],
   [0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0]]
   """
def caldistance():
    dist = [0 for i in xrange(len(d))]
    for i in xrange(1,len(d)):
        min_dis = 99999
        for j in xrange(i):
            if d[j][i] > 0:
                if dist[j] + d[j][i] < min_dis:
                    min_dis = dist[j] + d[j][i]
        if min_dis != 99999:
            dist[i] = min_dis
    return dist

if __name__ == '__main__':
    #print caldistance()
    a = -3.5678
    if float(a) < 0:
        print float(a)
