#coding=utf-8

import os
import pandas as pd
import matplotlib.pyplot as plt

"""
    kaggle的一个题目：https://www.kaggle.com/c/titanic/data
"""

def titanic(train_file, test_file):
    pf_train = pd.read_csv(train_file)
    #print(pf_train.columns)
    #print(pf_train.head())
    #print(pf_train.info())
    #print(pf_train.describe())

    fig = plt.figure()
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    fig.set(alpha=0.2) #设置图表颜色alpha参数

    plt.subplot2grid((2,3),(0,0)) #一张大图里分裂几个小图
    pf_train.Survived.value_counts().plot(kind='bar') # plots a bar graph of those who surived vs those who did not
    plt.title("获救情况（1为获救）")
    plt.ylabel("人数")

    plt.subplot2grid((2,3), (0,1))
    pf_train.Pclass.value_counts().plot(kind='bar')
    plt.title("乘客等级分布")
    plt.ylabel("人数")

    plt.subplot2grid((2,3), (0,2))
    plt.scatter(pf_train.Survived, pf_train.Age)
    plt.grid(b=True, which='major', axis='y')
    plt.title("年龄看获救分布（1为获救）")
    plt.ylabel("年龄")

    plt.subplot2grid((2,3), (1,0))
    pf_train.Age[pf_train.Pclass==1].plot(kind='kde')
    pf_train.Age[pf_train.Pclass==2].plot(kind='kde')
    pf_train.Age[pf_train.Pclass==3].plot(kind='kde')
    plt.xlabel("年龄")
    plt.ylabel("密度")
    plt.title("各等级的乘客年龄分布")
    plt.legend(("头等舱","2等仓","3等仓"), loc='best')

    plt




if __name__ == '__main__':
    train_file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'train.csv')
    test_file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test.csv')
    titanic(train_file_name, test_file_name)
