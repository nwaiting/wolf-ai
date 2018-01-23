#coding=utf-8
from texttable import Texttable
from numpy import *
import time
import xlrd

class CF:
    def __init__(self, movies, ratings, k=5, n=10):
        self.movies = movies
        self.ratings = ratings
        # 邻居个数
        self.k = k
        # 推荐个数
        self.n = n
        # 用户对物品的评分
        # 数据格式{'UserID：用户ID':[(ItemID：物品ID,Rating：用户的评分)]}
        self.userDict = {}
        # 对某物品评分的用户 数据格式：{'ItemID：物品ID',[UserID：用户ID]}
        # {'1',[1,2,3..],...}
        self.ItemUser = {}
        # 邻居的信息
        self.neighbors = []
        # 推荐列表
        self.recommandList = []
        self.cost = 0.0

    # 基于用户的推荐
    # 根据评分计算用户之间的相似度
    def recommendByUser(self, userId):
        self.formatRate()
        # 推荐个数 等于 本身评分个数，用户计算准确率
        self.n = len(self.userDict[userId])
        self.getNearestNeighbor(userId)
        self.getrecommandList(userId)
        self.getPrecision(userId)

    # 获取推荐列表
    def getrecommandList(self, userId):
        self.recommandList = []
        # 建立推荐字典
        recommandDict = {}
        for neighbor in self.neighbors:
            movies = self.userDict[neighbor[1]]
            for movie in movies:
                if(movie[0] in recommandDict):
                    recommandDict[movie[0]] += neighbor[0]
                else:
                    recommandDict[movie[0]] = neighbor[0]

        # 建立推荐列表
        for key in recommandDict:
            self.recommandList.append([recommandDict[key], key])
        self.recommandList.sort(reverse=True)
        self.recommandList = self.recommandList[:self.n]

    # 将ratings转换为userDict和ItemUser
    def formatRate(self):
        # 数据格式{'UserID：用户ID':[(ItemID：物品ID,Rating：用户的评分)]}
        self.userDict = {}
        # 数据格式：{'ItemID：物品ID',[UserID：用户ID]}
        self.ItemUser = {}
        for item in self.ratings:
            # 数据归一化
            self.userDict[item[0]] = [(j, float(item[j])/5) for j in range(1, len(item))]

        for j in range(1, len(self.ratings[0])):
            self.ItemUser[j] = [i[0] for i in self.ratings]
        return

    # 找到某用户的相邻用户
    def getNearestNeighbor(self, userId):
        neighbors = []
        self.neighbors = []
        # 获取userId评分的Item都有那些用户也评过分
        for i in self.userDict[userId]:
            for j in self.ItemUser[i[0]]:
                if(j != userId and j not in neighbors):
                    neighbors.append(j)
        # 计算这些用户与userId的相似度并排序
        for i in neighbors:
            dist = self.getCost(userId, i)
            self.neighbors.append([dist, i])
        # 排序默认是升序，reverse=True表示降序
        self.neighbors.sort(reverse=True)
        self.neighbors = self.neighbors[:self.k]

    # 格式化userDict数据
    def formatuserDict(self, userId, l):
        user = {}
        for i in self.userDict[userId]:
            user[i[0]] = [i[1], 0]
        for j in self.userDict[l]:
            if(j[0] not in user):
                user[j[0]] = [0, j[1]]
            else:
                user[j[0]][1] = j[1]
        return user

    # 计算余弦距离
    def getCost(self, userId, l):
        # 获取用户userId和l评分的并集
        # {'ItemID'：[userId的评分，l的评分]} 没有评分为0
        user = self.formatuserDict(userId, l)
        x = 0.0
        y = 0.0
        z = 0.0
        for k, v in user.items():
            x += float(v[0]) * float(v[0])
            y += float(v[1]) * float(v[1])
            z += float(v[0]) * float(v[1])
        if(z == 0.0):
            return 0
        return z / sqrt(x * y)

    # 推荐的准确率
    def getPrecision(self, userId):
        user = [i[0] for i in self.userDict[userId]]
        recommand = [i[1] for i in self.recommandList]
        count = 0.0
        if(len(user) >= len(recommand)):
            for i in recommand:
                if(i in user):
                    count += 1.0
            self.cost = count / len(recommand)
        else:
            for i in user:
                if(i in recommand):
                    count += 1.0
            self.cost = count / len(user)

    def showResult(self, user):
        with open('./outer/CollaborativeFiltering/data/result.data', 'ab+') as f:
            f.write(('{0} recommand list : \n'.format(user)).encode())
            f.write(('{0} {1}\n'.format(user, self.userDict[user])).encode())
            for item in self.neighbors:
                f.write(('{0} {1}\n'.format(item, self.userDict[item[1]])).encode())

def readxlrdFile(filename):
    data = []
    with xlrd.open_workbook(filename) as xlfd:
        table = xlfd.sheet_by_name('user_data')
        for i in range(table.nrows):
            if len(table.row_values(i)) > 0:
                res = table.row_values(i)[0].strip().strip('\r\n')
                res = res.replace('[','').replace(']','').replace(',','').split()
                data.append([res[0]+'-'+res[1]] + res[2:])
    return data

def readxlrdFile2(filename):
    data = []
    with xlrd.open_workbook(filename) as xlfd:
        table = xlfd.sheet_by_name('user_data')
        for i in range(table.nrows):
            tmp_list = []
            for j in table.row_values(i):
                if j:
                    tmp_list.append(j)
                else:
                    tmp_list.append(0)
            data.append(tmp_list[:])
    return data

def main():
    ratings = readxlrdFile('./outer/CollaborativeFiltering/data/train_data.xlsx')
    test_ratings = readxlrdFile2('./outer/CollaborativeFiltering/data/test_data.xlsx')
    itemIds = [[i,None] for i in range(1,len(ratings[0]))]
    for result_item in test_ratings:
        demo = CF(itemIds, ratings + [result_item], k=5)
        demo.recommendByUser(result_item[0])
        demo.showResult(result_item[0])

if __name__ == '__main__':
    main()
