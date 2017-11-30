# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 12:15:57 2017

@author: Administrator
"""

import math
import random
import copy
import pylab

try:
    import psyco
    psyco.full()
except ImportError as e:
    #print "import error {0}".format(e)
    pass

try:
    import xlrd
except Exception as e:
    print "import error {0}".format(e)

FLOAT_MAX = 1e100

points_arr_num = 0

class Point:
    #__slots__ = ["x", "y", "group", "membership"]
    def __init__(self, clusterCenterNumber, attr_size = 1, x = 0, y = 0, group = 0):
        self.x = [0.0 for _ in xrange(attr_size)]
        self.group = group
        self.membership = [0.0 for _ in range(clusterCenterNumber)]

def generatePoints(pointsNumber, radius, clusterCenterNumber):
    points = [Point(clusterCenterNumber, 1) for _ in range(2 * pointsNumber)]
    count = 0
    for point in points:
        count += 1
        r = random.random() * radius
        angle = random.random() * 2 * math.pi
        point.x = r * math.cos(angle)
        point.y = r * math.sin(angle)
        if count == pointsNumber - 1:
            break
    for index in range(pointsNumber, 2 * pointsNumber):
        points[index].x = 2 * radius * random.random() - radius
        points[index].y = 2 * radius * random.random() - radius
    return points

def genPoints(clusterCenterNumber, radius, dataFile):
    points = None
    try:
        with xlrd.open_workbook(dataFile) as xlfd:
            table = xlfd.sheet_by_name(u'Sheet6')
            print table.nrows, table.ncols
            arrt_num = table.ncols
            points_num = table.nrows
            points_arr_num = points_num
            #points = [Point(clusterCenterNumber, arrt_num) for _ in range(2 * points_num)]
            points = [Point(clusterCenterNumber, arrt_num) for _ in range(1 * points_num)]
            count = 0
            for point in points:
                point.x = table.row_values(count)
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
    #print len(pointA.x), len(pointB.x)
    for i in xrange(len(pointA.x)):
        total += pow(pointA.x[i] - pointB.x[i], 2)
    return total

def getNearestCenter(point, clusterCenterGroup):
    minIndex = point.group
    minDistance = FLOAT_MAX
    for index, center in enumerate(clusterCenterGroup):
        distance = solveDistanceBetweenPoints(point, center)
        if (distance < minDistance):
            minDistance = distance
            minIndex = index
    return (minIndex, minDistance)

def kMeansPlusPlus(points, clusterCenterGroup):
    clusterCenterGroup[0] = copy.copy(random.choice(points))
    distanceGroup = [0.0 for _ in range(len(points))]
    sum = 0.0
    for index in range(1, len(clusterCenterGroup)):
        for i, point in enumerate(points):
            distanceGroup[i] = getNearestCenter(point, clusterCenterGroup[:index])[1]
            sum += distanceGroup[i]
        sum *= random.random()
        for i, distance in enumerate(distanceGroup):
            sum -= distance;
            if sum < 0:
                clusterCenterGroup[index] = copy.copy(points[i])
                break
    return

def fuzzyCMeansClustering(points, clusterCenterNumber, weight):
    clusterCenterGroup = [Point(clusterCenterNumber, points_arr_num) for _ in range(clusterCenterNumber)]
    kMeansPlusPlus(points, clusterCenterGroup)
    clusterCenterTrace = [[clusterCenter] for clusterCenter in clusterCenterGroup]
    tolerableError, currentError = 1.0, FLOAT_MAX
    while currentError >= tolerableError:
        for point in points:
            getSingleMembership(point, clusterCenterGroup, weight)
        currentCenterGroup = [Point(clusterCenterNumber, points_arr_num) for _ in range(clusterCenterNumber)]
        for centerIndex, center in enumerate(currentCenterGroup):
            upperSum = [0.0 for _ in xrange(len(points[0].x))]
            lowerSum = 0.0
            for point in points:
                membershipWeight = pow(point.membership[centerIndex], weight)
                for k in xrange(len(point.x)):
                    upperSum[k] += point.x[k] * membershipWeight
                lowerSum += membershipWeight

            for k in xrange(len(center.x)):
                try:
                    center.x[k] = upperSum[k] / lowerSum
                except ZeroDivisionError as e:
                    print "erro {0} {1}".format(e, lowerSum)
        # update cluster center trace
        currentError = 0.0
        for index, singleTrace in enumerate(clusterCenterTrace):
            singleTrace.append(currentCenterGroup[index])
            currentError += solveDistanceBetweenPoints(singleTrace[-1], singleTrace[-2])
            clusterCenterGroup[index] = copy.copy(currentCenterGroup[index])
    for point in points:
        maxIndex, maxMembership = 0, 0.0
        for index, singleMembership in enumerate(point.membership):
            if singleMembership > maxMembership:
                maxMembership = singleMembership
                maxIndex = index
        point.group = maxIndex
    return clusterCenterGroup, clusterCenterTrace

def getSingleMembership(point, clusterCenterGroup, weight):
    distanceFromPoint2ClusterCenterGroup = [solveDistanceBetweenPoints(point, clusterCenterGroup[index]) for index in range(len(clusterCenterGroup))]
    for centerIndex, singleMembership in enumerate(point.membership):
        sum = 0.0
        isCoincide = [False, 0]
        for index, distance in enumerate(distanceFromPoint2ClusterCenterGroup):
            if distance == 0:
                isCoincide[0] = True
                isCoincide[1] = index
                break
            sum += pow(float(distanceFromPoint2ClusterCenterGroup[centerIndex] / distance), 1.0 / (weight - 1.0))
        if isCoincide[0]:
            if isCoincide[1] == centerIndex:
                point.membership[centerIndex] = 1.0
            else:
                point.membership[centerIndex] = 0.0
        else:
            point.membership[centerIndex] = 1.0 / sum

def showClusterAnalysisResults(points, clusterCenterTrace):
    for singleTrace in clusterCenterTrace:
        if len(singleTrace) > 0:
            print singleTrace[0].x
    """
    colorStore = ['or', 'og', 'ob', 'oc', 'om', 'oy', 'ok']
    pylab.figure(figsize=(9, 9), dpi = 80)
    for point in points:
        color = ''
        if point.group >= len(colorStore):
            color = colorStore[-1]
        else:
            color = colorStore[point.group]
        for i in xrange(len(point.x)):
            pylab.plot(point.x, color)

    for singleTrace in clusterCenterTrace:
        if len(singleTrace) > 0:
            print singleTrace[0].x
    pylab.show()
    """

if __name__ == '__main__':
    dataFile = './outer/fcm/data/user_vector.xlsx'
    # 族的个数
    clusterCenterNumber = 4
    pointsNumber = 2000
    radius = 10
    weight = 2
    #points = generatePoints(pointsNumber, radius, clusterCenterNumber)
    points = genPoints(clusterCenterNumber, radius, dataFile)
    _, clusterCenterTrace = fuzzyCMeansClustering(points, clusterCenterNumber, weight)
    showClusterAnalysisResults(points, clusterCenterTrace)
