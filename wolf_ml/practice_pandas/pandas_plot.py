#coding=utf-8

import pandas as pd
import matplotlib.pyplot as plt

"""
    横向柱形图（条形图）
    把ax.bar( ) 换成ax.barh( )即可
"""

def main():
    data = [[1,2,3,4],[1, 2, 2, 3],[4,3,2,1],[4,3,2,1],[4,3,2,1]]
    df2 = pd.DataFrame(data=data, columns=["A","B","C","D"], index=["a","b","c","d","e"])
    #df2.plot(kind="barh") #横向柱形图
    df2.plot(kind="bar") #竖向柱形图
    plt.show()

def f1():
    """
        直接用bar进行叠加的话，可以使用:
            year = [1,1,1,1,1,1]
            v1 = [2,2,2,2,2,2]
            ax.bar(year,v1,color="green")
            ax.bar(year,v2,color="red")
            ax.bar(year,v3,color="blue")
            ax.legend(["first place","second place","third place"])  #设置图例
            plt.show()
    """

    data = [[1,2,3,4],[1, 2, 2, 3],[4,3,2,1],[4,3,2,1],[4,3,2,1]]
    labels = ["A","B","C","D"]
    y = ["a","b","c","d","e"]
    plt.bar(data, y, label=labels)
    plt.show()

    left = pd.DataFrame({'id':[1,2,3,4,5],
            'Name': ['Alex', 'Amy', 'Allen', 'Alice', 'Ayoung'],
            'subject_id':['sub1','sub2','sub4','sub6','sub6']}
            )
    print(left["Name"].values.tolist())

if __name__ == '__main__':
    main()
    #f1()
