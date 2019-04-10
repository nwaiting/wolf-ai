#coding=utf-8


"""
    StratifiedKFold用法类似Kfold，但是他是分层采样，确保训练集，测试集中各类别样本的比例与原始数据集中相同
    KFold：
        申明：
            sklearn.model_selection.KFold(n_splits=3, shuffle=False, random_state=None)
        参数：
            n_splits：表示划分几等份
            shuffle：在每次划分时，是否进行洗牌
                1、若为Falses时，其效果等同于random_state等于整数，每次划分的结果相同
                2、若为True时，每次划分的结果都不一样，表示经过洗牌，随机取样的
            random_state：随机种子数
"""

import numpy as np
from sklearn.model_selection import KFold,StratifiedKFold,ShuffleSplit,StratifiedShuffleSplit


def main():
    X=np.array([
            [1,2,3,4],
            [11,12,13,14],
            [21,22,23,24],
            [31,32,33,34],
            [41,42,43,44],
            [51,52,53,54],
            [61,62,63,64],
            [71,72,73,74]
            ])
    y=np.array([1,1,0,0,1,1,0,0])

    kfolder = KFold(n_splits=4, shuffle=False)
    for train,test in kfolder.split(X,y):
        print("train {0} | test {1}".format(train, test))
    print("=="*64)

    skfolder = StratifiedKFold(n_splits=4, shuffle=False)
    for train,test in skfolder.split(X,y):
        print("train {0} | test {1}".format(train, test))














if __name__ == '__main__':
    main()
