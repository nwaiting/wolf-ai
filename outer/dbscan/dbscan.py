# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 21:22:26 2017

@author: Administrator
"""

import math
import random
import copy
import pylab

try:
    import psyco
    psyco.full()
except ImportError:
    pass

try:
    import xlrd
except Exception as e:
    print "import error {0}".format(e)

FLOAT_MAX = 1e100

CORE_POINT_TYPE = -2
BOUNDARY_POINT_TYPE = 1 #ALL NONE-NEGATIVE INTEGERS CAN BE BOUNDARY POINT TYPE
OTHER_POINT_TYPE = -1

class Point:
    #__slots__ = ["x", "y", "group", "pointType"]
    def __init__(self, attr_size = 1, x = 0, y = 0, group = 0, pointType = -1):
        self.name = None
        self.x = [0.0 for _ in xrange(attr_size)]
        self.group = group
        self.pointType = pointType

"""
class Point:
    #__slots__ = ["x", "y", "group", "membership"]
    def __init__(self, clusterCenterNumber, attr_size = 1, x = 0, y = 0, group = 0):
        self.name = None
        self.x = [0.0 for _ in xrange(attr_size)]
        self.group = group
        self.membership = [0.0 for _ in range(clusterCenterNumber)]
"""

def generatePoints(pointsNumber, radius):
    points = [Point() for _ in range(4 * pointsNumber)]
    originX = [-radius, -radius, radius, radius]
    originY = [-radius, radius, -radius, radius]
    count = 0
    countCenter = 0
    for index, point in enumerate(points):
        count += 1
        r = random.random() * radius
        angle = random.random() * 2 * math.pi
        point.x = r * math.cos(angle) + originX[countCenter]
        point.y = r * math.sin(angle) + originY[countCenter]
        point.group = index
        if count >= pointsNumber * (countCenter + 1):
            countCenter += 1
    return points

def genPoints(clusterCenterNumber, radius, dataFile):
    points = None
    try:
        with xlrd.open_workbook(dataFile) as xlfd:
            table = xlfd.sheet_by_name(u'user_matrix_data')
            print table.nrows, table.ncols
            arrt_num = table.ncols - 1
            points_num = table.nrows
            points_arr_num = points_num
            #points = [Point(clusterCenterNumber, arrt_num) for _ in range(2 * points_num)]
            points = [Point(arrt_num) for _ in range(1 * points_num)]
            count = 0
            for point in points:
                rdata = table.row_values(count)
                point.name = rdata[0]
                point.x = rdata[1:]
                if count == points_num - 1:
                    break
                count += 1
            #for index in range(points_num, 2 * points_num):
            #    points[index].x = [random.choice(points[0].x) for _ in xrange(arrt_num)]
    except Exception as e:
        print "error {0}".format(e)
    return points

def solveDistanceBetweenPoints(pointA, pointB):
    total = 0.0
    for i in xrange(len(pointA.x)):
        total += pow(pointA.x[i] - pointB.x[i])
    return total
    #return (pointA.x - pointB.x) * (pointA.x - pointB.x) + (pointA.y - pointB.y) * (pointA.y - pointB.y)

def isInPointBoundary(centerPoint, customPoint, halfScale):
    flag = True
    for i in xrange(len(centerPoint.x)):
        flag &= customPoint.x[i] <= centerPoint.x[i] + halfScale and customPoint.x[i] >= centerPoint.x[i] - halfScale
    return flag
    #return customPoint.x <= centerPoint.x + halfScale and customPoint.x >= centerPoint.x - halfScale and customPoint.y <= centerPoint.y + halfScale and customPoint.y >= centerPoint.y - halfScale

def getPointsNumberWithinBoundary(points, halfScale):
    pointsIndexGroupWithinBoundary = [[] for _ in range(len(points))]
    for centerIndex, centerPoint in enumerate(points):
        for index, customPoint in enumerate(points):
            if centerIndex != index and isInPointBoundary(centerPoint, customPoint, halfScale):
                pointsIndexGroupWithinBoundary[centerIndex].append(index)
    return pointsIndexGroupWithinBoundary

def decidePointsType(points, pointsIndexGroupWithinBoundary, minPointsNumber):
    for index, customPointsGroup in enumerate(pointsIndexGroupWithinBoundary):
        if len(customPointsGroup) >= minPointsNumber:
            points[index].pointType = CORE_POINT_TYPE
    for index, customPointsGroup in enumerate(pointsIndexGroupWithinBoundary):
        if len(customPointsGroup) < minPointsNumber:
            for customPointIndex in customPointsGroup:
                if points[customPointIndex].pointType == CORE_POINT_TYPE:
                    points[index].pointType = customPointIndex

def mergeGroup(points, fromIndex, toIndex):
    for point in points:
        if point.group == fromIndex:
            point.group = toIndex

def dbscan(points, pointsIndexGroupWithinBoundary, clusterCenterNumber):
    countGroupsNumber = {index: 1 for index in range(len(points))}
    for index, point in enumerate(points):
        if point.pointType == CORE_POINT_TYPE:
            for customPointIndex in pointsIndexGroupWithinBoundary[index]:
                if points[customPointIndex].pointType == CORE_POINT_TYPE and points[customPointIndex].group != point.group:
                    countGroupsNumber[point.group] += countGroupsNumber[points[customPointIndex].group]
                    del countGroupsNumber[points[customPointIndex].group]
                    mergeGroup(points, points[customPointIndex].group, point.group)
        #point.pointType >= 0 means it is BOUNDARY_POINT_TYPE
        elif point.pointType >= 0:
            corePointGroupIndex = points[point.pointType].group
            if countGroupsNumber.has_key(corePointGroupIndex) and countGroupsNumber.has_key(point.group):
                countGroupsNumber[corePointGroupIndex] += countGroupsNumber[point.group]
                del countGroupsNumber[point.group]
            point.group = corePointGroupIndex
    countGroupsNumber = sorted(countGroupsNumber.iteritems(), key=lambda group: group[1], reverse=True)
    count = 0
    for key, _ in countGroupsNumber:
        count += 1
        for point in points:
            if point.group == key:
                point.group = -1 * count
        if count >= clusterCenterNumber:
            break

def showClusterAnalysisResults(points):
    for item in points:
        if item.group > 0:
            print "====== {0} {1} {2}".format(item.group, item.name, item.x)
        else:
            print "{0} {1} {2}".format(item.group, item.name, item.x)
    return
    colorStore = ['or', 'og', 'ob', 'oc', 'om', 'oy', 'ok']
    pylab.figure(figsize=(9, 9), dpi = 80)
    for point in points:
        color = ''
        if point.group < 0:
            color = colorStore[-1 * point.group - 1]
        else:
            color = colorStore[-1]
        pylab.plot(point.x, point.y, color)
    pylab.show()


if __name__ == '__main__':
    dataFile = './outer/fcm/data/user_matrix.xlsx'
    clusterCenterNumber = 8
    pointsNumber = 500
    radius = 10
    Eps = 2
    minPointsNumber = 18
    #points = generatePoints(pointsNumber, radius)
    points = genPoints(clusterCenterNumber, radius, dataFile)
    pointsIndexGroupWithinBoundary = getPointsNumberWithinBoundary(points, Eps)
    decidePointsType(points, pointsIndexGroupWithinBoundary, minPointsNumber)
    dbscan(points, pointsIndexGroupWithinBoundary, clusterCenterNumber)
    showClusterAnalysisResults(points)
