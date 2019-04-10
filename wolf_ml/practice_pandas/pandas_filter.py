#coding=utf-8



import pandas as pd


def main():
    df = pd.DataFrame({'Team': ['Riders', 'Riders', 'Devils', 'Devils', 'Kings','kings', 'Kings', 'Kings', 'Riders', 'Royals', 'Royals', 'Riders'],
        'Rank': [1,2,2,3,3,4,1,1,2,4,1,2],
        'Year': [2014,2015,2014,2015,2014,2015,2016,2017,2016,2014,2015,2017],
        'Points':[876,789,863,673,741,812,756,788,694,701,804,690],
        'Survived_Team':[0,1,1,0,0,0,0,1,1,1,1,0],
        'Survived_Team_1':[0,1,1,0,0,0,0,1,1,1,1,0]}
        )
    print(df)
    print("=="*64)
    # filter过滤后，会有标签和索引
    df_filter = df.filter(regex="(^Survived_Team_)|Ran*|^Tea*", axis=1) # select columns by regular expression
    print(df_filter)
    print("1=="*64)

    df_filter = df.filter(regex="Survived_Team_.*", axis=1) # select columns by regular expression
    print(df_filter)
    print("2=="*64)

    df_filter = df.filter(regex="(^Survived_Team_)|Ran*|^Tea*", axis=1) # select columns by regular expression
    print(df_filter)
    print("22=="*64)

    df_filter = df.filter(like="Survived_Team_", axis=1) #select columns
    print(df_filter)
    print("3=="*64)

    df_filter = df.filter(items=['Rank', 'Tea'], axis=1) #select columns
    print(df_filter)
    print("4=="*64)
    #print(df_filter.as_matrix())








if __name__ == '__main__':
    main()
