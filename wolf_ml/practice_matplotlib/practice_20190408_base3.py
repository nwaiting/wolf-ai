#coding=utf-8

import numpy as np
import matplotlib.pyplot as plt


def f1():
    """
        显示中文
        subplots绘图时 设置总标题 ：fig.suptitle(name)
        子图设置标签和标题


        有的notebook里面需要设置两行才能显示中文：
            plt.rcParams['font.family'] = ['sans-serif']
            plt.rcParams['font.sans-serif'] = ['SimHei']
    """

    fig = plt.figure()
    fig.set(alpha=0.2)
    """
        显示中文方法1：
            简洁的用法。缺点：污染全局字体设置。（所以需要第二步骤）
            不需要对字体路径硬编码，而且一次设置，多次使用，更方便
    """
    #plt.rcParams['font.sans-serif'] = ['SimHei'] # 步骤一（替换sans-serif字体）
    #plt.rcParams['axes.unicode_minus'] = False   # 步骤二（解决坐标轴负数的负号显示问题）

    """
        显示中文方法2：
            rc
            不需要对字体路径硬编码，而且一次设置，多次使用，更方便
    """
    #plt.rc("font",{'family':'SimHei','size':'16'}) #步骤一（设置字体的更多属性）
    #plt.rc("axes",{"unicode_minus":False}) #步骤二（解决坐标轴负数的负号显示问题）

    x = np.arange(0,100)
    ax1 = plt.subplot2grid((3,3),(0,0))
    ax1.plot(x, np.log1p(x), label="log(x+1)")
    """
        显示中文方法3：
            直接在函数中设置属性，用时才设置，且不会污染全局字体设置，更灵活
            font = FontProperties(fname='/System/Library/Fonts/STHeiti Light.ttc', size=16)

            plt.xlabel("x轴")
            plt.ylabel("y轴", fontproperties=font) # 步骤一    （宋体）
            plt.title("标题", fontproperties=font) #          （黑体）

            或者
            plt.title("标题", fontproperties=SimHei) #          （黑体）
    """
    ax1.set_title(u"对数", fontproperties="SimHei")
    plt.ylabel("log")
    plt.xlabel("x")
    ax1.legend(loc="upper left")
    plt.show()


def f2():
    """
        翻转反向坐标轴
    """
    fig = plt.figure()
    fig.set(alpha=0.2)
    plt.rcParams['font.sans-serif'] = ['SimHei'] # 步骤一（替换sans-serif字体）
    plt.rcParams['axes.unicode_minus'] = False   # 步骤二（解决坐标轴负数的负号显示问题）
    x = np.arange(0,100)
    ax1 = plt.subplot2grid((3,3),(0,0))
    ax1.plot(x, np.log1p(x), label="log(x+1)")
    ax1.set_title(u"对数", fontproperties="SimHei")
    plt.ylabel("log")
    plt.xlabel("x")
    ax1.legend(loc="upper left")


    ax2 = plt.subplot2grid((3,3),(0,1))
    ax2.plot(x, np.log1p(x), label="log(x+1)")
    ax2.set_title(u"对数2", fontproperties="SimHei")
    plt.gca().invert_yaxis()
    plt.ylabel("log2")
    plt.xlabel("x")
    ax2.legend(loc="upper left")
    plt.show()


def f3():
    """
        bar柱形图的使用，以及叠加
            data = np.array([[10., 30., 19., 22.],
                    [5., 18., 15., 20.],
                    [4., 6., 3., 5.]])
            for i in range(data.shape[0]):#i表示list的索引值
                ax2.bar(X, data[i],
                        width=0.2,
                        bottom = np.sum(data[:i], axis = 0),
                        color = color_list[i % len(color_list)],
                        alpha =0.5)

        或者：
            year = [1,1,1,1,1,1]
            v1 = [2,2,2,2,2,2]
            v2 = [2,2,2,2,2,2]
            v3 = [2,2,2,2,2,2]
            ax.bar(year,v1,color="green")
            ax.bar(year,v2,color="red")
            ax.bar(year,v3,color="blue")
            ax.legend(["first place","second place","third place"])  #设置图例
            plt.show()
    """
    pass


if __name__ == '__main__':
    #f1()
    f2()
