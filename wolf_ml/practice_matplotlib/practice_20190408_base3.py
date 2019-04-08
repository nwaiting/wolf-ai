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




















if __name__ == '__main__':
    f1()
