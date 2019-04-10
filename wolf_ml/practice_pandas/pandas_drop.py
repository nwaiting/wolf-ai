#coding=utf-8



"""
    drop删除行、删除列
        print frame.drop(['a'])
        print frame.drop(['Ohio'], axis = 1)
"""


import numpy as np
import pandas as pd



def main():
    df = pd.DataFrame({'Team': ['Riders', 'Riders', 'Devils', 'Devils', 'Kings','kings', 'Kings', 'Kings', 'Riders', 'Royals', 'Royals', 'Riders'],
        'Rank': [1, 2, 2, 3, 3,4 ,1 ,1,2 , 4,1,2],
        'Year': [2014,2015,2014,2015,2014,2015,2016,2017,2016,2014,2015,2017],
        'Points':[876,789,863,673,741,812,756,788,694,701,804,690]}
        )
    print(df)
    print("=="*64)

    print(df.drop([1])) #删除行
    print("=="*64)

    print(df.drop(["Team"],axis=1)) #删除列
    print("=="*64)












if __name__ == '__main__':
    main()
