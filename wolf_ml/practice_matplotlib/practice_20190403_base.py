#coding=utf-8

import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

def test_version():
    import platform
    print(platform.python_version())

def main():
    """
        这个.plot需要许多参数，但前两个是'x'和'y'坐标，我们放入列表。 这意味着，根据这些列表我们拥有 3 个坐标：1,5 2,7和3,4
    """
    plt.plot([1,2,3],[5,7,4])
    plt.show()


def f1():
    """
        图例、标题和标签，多个图例放在一起
        注：轴域（Axes）即两条坐标轴围城的区域
    """
    x1 = [1,2,3]
    y1 = [5,7,4]

    x2 = [1,2,3]
    y2 = [10,14,12]

    l1 = plt.plot(x1, y1, label='First Line')
    l2 = plt.plot(x2, y2, label='Second Line')

    plt.xlabel('Plot Number')
    plt.ylabel('Important var')
    plt.title('Interesting Graph\nCheck it out')

    # 两种方法将多个图例放在一起
    #plt.legend()
    plt.legend([l1, l2], ['first', 'second'], loc = 'upper right')

    plt.show()


def f2():
    """
        条形图、直方图
    """
    x1 = [1,3,5,7,9]
    y1 = [5,2,7,8,2]
    x2 = [2,4,6,8,10]
    y2 = [8,6,2,5,6]
    # 自定义颜色，你可以在任何类型的绘图中使用颜色，例如g为绿色，b为蓝色，r为红色，等等。 你还可以使用十六进制颜色代码，如#191970
    plt.bar(x1,y1, label="Example one", color='b')
    plt.bar(x2,y2, label="Example two", color='r')
    plt.legend()
    plt.xlabel('bar number')
    plt.ylabel('bar height')
    plt.title('Epic Graph\nAnother Line! Whoa')
    plt.show()


def f3():
    """
        直方图
            统计直方图，统计bins每个桶里面有多少个值
    """
    population_ages = [22,55,62,45,21,22,34,42,42,4,99,102,110,120,121,122,130,111,115,112,80,75,65,54,44,43,42,48]
    bins = [0,10,20,30,40,50,60,70,80,90,100,110,120,130]
    plt.hist(population_ages, bins, histtype='bar', rwidth=0.8)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Interesting Graph\nCheck it out')
    plt.legend()
    plt.show()


def f4():
    """
        散点图
            散点图通常用于比较两个变量来寻找相关性或分组，如果你在 3 维绘制则是 3 个
    """
    x = [1,2,3,4,5,6,7,8]
    y = [5,2,4,2,1,4,5,2]

    # plt.scatter不仅允许我们绘制x和y，而且还可以让我们决定所使用的标记颜色，大小和类型。 有一堆标记选项
    #plt.scatter(x,y, label='skitscat', color='k', s=25, marker="o")
    plt.scatter(x,y, color='k', s=25, marker="o")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Interesting Graph\nCheck it out')
    #plt.legend()
    plt.show()


def f5():
    """
        堆叠图
            堆叠图用于显示『部分对整体』随时间的关系。 堆叠图基本上类似于饼图，只是随时间而变化
    """
    days =      [1,2,3,4,5]

    sleeping =  [7,8,6,11,7]
    eating =    [2,3,4,3,2]
    working =   [7,8,7,2,2]
    playing =   [8,5,7,8,13]
    y = [sleeping,eating,working,playing]
    # 我们的x轴将包括day变量，即 1, 2, 3, 4 和 5。然后，日期的各个成分保存在它们各自的活动中。

    plt.stackplot(days, sleeping,eating,working,playing,labels=['Sleeping','Eating','Working','Playing'], colors=['m','c','r','k'])
    #plt.stackplot(days, y,labels=['Sleeping','Eating','Working','Playing'], colors=['m','c','r','k'])
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Interesting Graph\nCheck it out')
    # 为了显示颜色的小图标
    plt.legend(loc='upper right')
    plt.show()


def f6():
    """
        饼图
            饼图很像堆叠图，只是它们位于某个时间点。 通常，饼图用于显示部分对于整体的情况，通常以％为单位。 幸运的是，Matplotlib 会处理切片大小以及一切事情，我们只需要提供数值
    """
    slices = [7,2,2,13]
    activities = ['sleeping','eating','working','playing']
    cols = ['c','m','r','b']

    """
        需要指定『切片』，这是每个部分的相对大小
        指定相应切片的颜色列表。
        可以选择指定图形的『起始角度』。 这使你可以在任何地方开始绘图。 在我们的例子中，我们为饼图选择了 90 度角，这意味着第一个部分是一个竖直线条。
        可以选择给绘图添加一个字符大小的阴影，然后我们甚至可以使用explode拉出一个切片。

        切片拉出：
            总共有四个切片，所以对于explode，如果我们不想拉出任何切片，我们传入0,0,0,0。 如果我们想要拉出第一个切片，我们传入0.1,0,0,0
        使用autopct，选择将百分比放置到图表上面
    """
    plt.pie(slices,
            labels=activities,
            colors=cols,
            startangle=180,
            shadow= True,
            explode=(0,0,0,0),
            autopct='%1.1f%%')

    plt.title('Interesting Graph\nCheck it out')
    plt.show()


def f7():
    """
        填充
    """
    x = range(1,16)
    y = [3.990,3.970,3.980,4.030,3.930,3.970,3.980,3.950,3.940,3.930,3.980,3.990,4.000,4.010,4.020]
    #plt.plot_date(x,y,'-',label='Price')
    plt.plot(x,y,'-',label="Price")
    plt.xlabel("date")
    plt.ylabel("Price")
    plt.title('Interesting Graph\nCheck it out')
    #plt.legend()
    plt.show()

def f8():
    """
        子图
            讨论一些可能的图表自定义。 为了开始修改子图，我们必须定义它们。 我们很快会谈论他们，但有两种定义并构造子图的主要方法。 现在，我们只使用其中一个，但我们会很快解释它们。
    """
    x = range(1,46)
    y = [3.990,3.970,3.980,4.030,3.930,3.970,3.980,3.950,3.940,3.930,3.980,3.990,4.000,4.010,4.020,3.990,3.970,3.980,4.030,3.930,3.970,3.980,3.950,3.940,3.930,3.980,3.990,4.000,4.010,4.020,3.990,3.970,3.980,4.030,3.930,3.970,3.980,3.950,3.940,3.930,3.980,3.990,4.000,4.010,4.020]
    fig = plt.figure()
    ax1 = plt.subplot2grid((1,1), (0,0))
    ax1.plot(x,y,'-',label="Price")

    # 显示横坐标显示的倾斜角度， 由于我们正在绘制日期，我们可能会发现，如果我们放大，日期会在水平方向上移动。但是，我们可以自定义这些刻度标签，
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(30)
    # 这将使标签转动到对角线方向。 接下来，我们可以添加一个网格
    ax1.grid(True)#, color='g', linestyle='-', linewidth=5)

    # 更改标签颜色。 我们可以通过修改我们的轴对象来实现
    ax1.xaxis.label.set_color('c')
    ax1.yaxis.label.set_color('r')

    # 要显示的轴指定具体数字，而不是像这样的自动选择
    #ax1.set_yticks([2,3,4,5])
    ax1.set_ylim(3.9,4.1)
    ymajorLocator = MultipleLocator(0.01) #将y轴主刻度标签设置为0.5的倍数
    ymajorFormatter = FormatStrFormatter('%1.2f') #设置y轴标签文本的格式
    ax1.yaxis.set_major_locator(ymajorLocator)
    ax1.yaxis.set_major_formatter(ymajorFormatter)

    """
    填充 填充所做的事情，是在变量和你选择的一个数值之间填充颜色，中间那个数字就是从3.96开始到y之间的距离填充，所以填充的画面可能在上面，可能在下面
    plt.fill_between(x，y1，y2，where=条件表达式, color=颜色，alpha=透明度)
    plt.fill_between(
        x, y1, y2=0, where=None,
        interpolate=False, step=None,
        hold=None, data=None,
        **kwargs
        )

    """
    # 有些点在两部分间交错，所以有些没有画出来
    base_split = 0.5

    # 增加显示的小图标
    ax1.plot([],[],linewidth=5, label='loss', color='r',alpha=0.5)
    ax1.plot([],[],linewidth=5, label='gain', color='g',alpha=0.5)

    #ax1.fill_between(x, base_split, y, facecolor='r')
    ax1.fill_between(x, base_split, y, where=[i > base_split for i in y], facecolor='b')
    ax1.fill_between(x, base_split, y, where=[i < base_split for i in y], facecolor='r', alpha=0.5)

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('jingdongfang')
    plt.legend()
    # 可能需要略微调整绘图，因为日期跑到了图表外面。 记不记得我们在第一篇教程中讨论的configure subplots按钮？ 我们不仅可以以这种方式配置图表，我们还可以在代码中配置它们
    plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
    plt.show()


def f9():
    """
        边框和水平线条
            高斯曲线
    """
    mu = 0  #均值
    sigma = 1 #方差
    sig = math.sqrt(0.2)  # 标准差δ
    x = np.linspace(mu - 3*sig, mu + 3*sig, 500)
    y = np.exp((-(x - mu) ** 2 - 0.5 * (x - 3) ** 2 - 0.5 * (x + 3) ** 2)/(2* sig **2))/(math.sqrt(2*math.pi)*sig)
    plt.plot(y)
    plt.show()


def f10():
    def f(x,y):
        return (1-x/2+x**5+y**3)*np.exp(-x**2-y**2)

    n = 256
    x = np.linspace(-3,3,n)
    y = np.linspace(-3,3,n)
    X,Y = np.meshgrid(x,y)

    plt.contourf(X, Y, f(X,Y), 8, alpha=.75, cmap='jet')
    C = plt.contour(X, Y, f(X,Y), 8, colors='black', linewidth=.5)
    plt.show()

if __name__ == '__main__':
    #main()
    #f1()
    #f2()
    #f3()
    #f4()
    #f5()
    #f6()
    #f7()
    #f8()
    #f9()
    f10()
