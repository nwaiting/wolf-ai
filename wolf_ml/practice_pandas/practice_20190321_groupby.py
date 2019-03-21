#coding=utf-8



"""
    任何分组(groupby)操作都涉及原始对象的以下操作之一
        分割对象
        应用一个函数
        结合的结果

    Pandas对象可以分成任何对象。有多种方式来拆分对象，如 -
        obj.groupby(‘key’)
        obj.groupby([‘key1’,’key2’])
        obj.groupby(key,axis=1)

    在许多情况下，我们将数据分成多个集合，并在每个子集上应用一些函数。在应用函数中，可以执行以下操作
        聚合 - 计算汇总统计
        转换 - 执行一些特定于组的操作
        过滤 - 在某些情况下丢弃数据
"""

import numpy as np
import pandas as pd




def main():
    df = pd.DataFrame({'Team': ['Riders', 'Riders', 'Devils', 'Devils', 'Kings','kings', 'Kings', 'Kings', 'Riders', 'Royals', 'Royals', 'Riders'],
        'Rank': [1, 2, 2, 3, 3,4 ,1 ,1,2 , 4,1,2],
        'Year': [2014,2015,2014,2015,2014,2015,2016,2017,2016,2014,2015,2017],
        'Points':[876,789,863,673,741,812,756,788,694,701,804,690]})
    print(df)
    print("=="*32)

    print(df.groupby('Team')) #返回的是一个对象
    print("=="*32)
    print(df.groupby('Team').groups)
    print("=="*32)
    #多列进行分组
    print(df.groupby(['Team','Year']).groups)
    print("=="*32)

    #遍历分组
    for name,group in df.groupby('Team'):
        print("k={},v={}".format(name,group))
    print("=="*32)

    # 选择一个分组
    grouped = df.groupby('Team')
    print(grouped.get_group('Devils'))

    # 聚合
    # 聚合函数为每个组返回单个聚合值。当创建了分组(group by)对象，就可以对分组数据执行多个聚合操作。一个比较常用的是通过聚合或等效的agg方法聚合
    grouped = df.groupby('Team')
    print(grouped['Points'].agg(np.mean))
    print('='*64)
    # 查看每一个分组的大小
    print(grouped.agg(np.size))
    print('='*64)

    # 一次应用多个聚合函数
    # 通过分组系列，还可以传递函数的列表或字典来进行聚合，并生成DataFrame作为输出
    grouped = df.groupby('Team')
    print(grouped['Points'].agg([np.sum, np.mean, np.std]))
    print('='*64)

    # 转换
    #分组或列上的转换返回索引大小与被分组的索引相同的对象。因此，转换应该返回与组块大小相同的结果
    grouped = df.groupby('Team')
    score_handle = lambda x:(x-x.mean())/x.std()*10
    print(grouped.transform(score_handle))
    print('='*64)

    # 过滤
    # 过滤根据定义的标准过滤数据并返回数据的子集。filter()函数用于过滤数据
    filtered = df.groupby('Team').filter(lambda x:len(x)>=3) #要求返回参加3次以上的队伍
    print(filtered)
    print('='*64)






















if __name__ == '__main__':
    main()
