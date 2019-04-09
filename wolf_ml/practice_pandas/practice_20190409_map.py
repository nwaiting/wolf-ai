#coding=utf-8

"""
    map
"""

import numpy as np
import pandas as pd



def main():
    df = pd.DataFrame({'Team': ['Riders', 'Riders', 'Devils', 'Devils', 'Kings','kings', 'Kings', 'Kings', 'Riders', 'Royals', 'Royals', 'Riders'],
        'Rank': [1,2,2,3,3,4,1,1,2,4,1,2],
        'Year': [2014,2015,2014,2015,2014,2015,2016,2017,2016,2014,2015,2017],
        'Points':[876,789,863,673,741,812,756,788,694,701,804,690],
        'Survived':[0,1,1,0,0,0,0,1,1,1,1,0]}
        )
    print(df)
    print("=="*64)
    # 对应的两列值作为str相加
    df["Team_Survived"] = df.Team + "_" + df.Survived.map(str)
    print(df)










if __name__ == '__main__':
    main()
