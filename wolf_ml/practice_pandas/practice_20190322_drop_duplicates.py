#coding=utf-8



"""
    删除某一列中重复的元素
    这个drop_duplicate方法是对DataFrame格式的数据，去除特定列下面的重复行。返回DataFrame格式的数据
        DataFrame.drop_duplicates(subset=None, keep='first', inplace=False)
            subset : column label or sequence of labels, optional
            用来指定特定的列，默认所有列
            keep : {‘first’, ‘last’, False}, default ‘first’
            删除重复项并保留第一次出现的项
            inplace : boolean, default False
            是直接在原来数据上修改还是保留一个副本
"""

import pandas as pd
import numpy as np



def main():
    df = pd.DataFrame({'Team': ['Riders', 'Riders', 'Devils', 'Devils', 'Kings','kings', 'Kings', 'Kings', 'Riders', 'Royals', 'Royals', 'Riders'],
        'Rank': [1, 2, 2, 3, 3,4 ,1 ,1,2 , 4,1,2],
        'Year': [2014,2015,2014,2015,2014,2015,2016,2017,2016,2014,2015,2017],
        'Points':[876,789,863,673,741,812,756,788,694,701,804,690]}
        )

    print(df)
    print(df.drop_duplicates("Year"))
    print("=="*64)












if __name__ == '__main__':
    main()
