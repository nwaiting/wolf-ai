# coding=utf-8

import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from matplotlib.animation import FuncAnimation


"""

    默认图，调用情况：
        默认情况下，
        matplotlib 会调用 gca() 来获取当前轴（axes）
        gca 调用 gcf() 来获取当前 figure，如果没有 figure，它便会调用 figure() 来创建一个，严格地说是创建一个 subplot
"""


def f1():
    #创建自定义图像
    fig = plt.figure(figsize=(4, 3), facecolor='blue')
    plt.show()


def f2():
    """
        基础设置属性操作
    """
    X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
    C, S = np.cos(X), np.sin(X)

    # 创建自定义图像 设置图片大小，属性等
    # plt.figure(figsize=(10, 6), dpi=80, facecolor='blue')
    plt.figure(figsize=(10, 6), dpi=100)

    # 设置线条属性 添加图例
    plt.plot(X, C, color="blue", linewidth=5, linestyle="-", label="cosine")
    plt.plot(X, S, color="red", linewidth=5, linestyle="-", label="sine")

    # 设置边界
    plt.xlim(X.min() * 1.1, X.max() * 1.1)
    #plt.xlim(-5, 5)
    plt.ylim(C.min() * 1.1, C.max() * 1.1)

    # 设置单位长度
    plt.xticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi])
    plt.yticks([-1, 0, +1])

    # 设置坐标轴显示单位 \pi转义为π
    plt.xticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi],
               [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])

    plt.yticks([-1, 0, +1],
               [r'$-1$', r'$0$', r'$+1$'])

    # 移动脊
    """
        脊（Spines）是连接轴刻度和提示边界的线。它们可以被放置在任意的位置，现在它们在边界上。我们将把它放到中心。
        因为有四个脊（顶部/底部/左边/右边），我们将通过设置颜色为 "none" 来隐藏他们，同时我们将移动底部和左边的两个到坐标为0的位置
    """
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data', 0))
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data', 0))

    # 添加注释点
    t = 2 * np.pi / 3
    plt.plot([t, t], [0, np.cos(t)], color='blue', linewidth=1.5, linestyle="--")
    plt.scatter([t, ], [np.cos(t), ], 50, color='blue')

    plt.annotate(r'$\sin(\frac{2\pi}{3})=\frac{\sqrt{3}}{2}$',
                 xy=(t, np.sin(t)), xycoords='data',
                 xytext=(+10, +30), textcoords='offset points', fontsize=16,
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

    plt.plot([t, t], [0, np.sin(t)], color='red', linewidth=1.5, linestyle="--")
    plt.scatter([t, ], [np.sin(t), ], 50, color='red')

    plt.annotate(r'$\cos(\frac{2\pi}{3})=-\frac{1}{2}$',
                 xy=(t, np.cos(t)), xycoords='data',
                 xytext=(-90, -50), textcoords='offset points', fontsize=16,
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

    # 设置透明度，显示出坐标数字
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontsize(16)
        label.set_bbox(dict(facecolor='white', edgecolor='None', alpha=0.65))

    # 添加图例
    plt.legend(loc='upper left', frameon=False)
    plt.show()


def f3():
    """
        图（Figures）, 子坐标（Subplots）, 轴(Axes) 和 Ticks
            f2()中使用隐式图和轴的创建（implicit figure and axes creation）来快速的绘图，但我们能通过 figure, subplot, 和 axes explicitly 进一步控制绘图
            我们已经在没有正式称呼使用 figures 和 subplots 的情况下使用了他们。当我们调用 plot，matplotlib 会调用 gca() 来获取当前轴（axes），
            同时 gca 调用 gcf() 来获取当前 figure，如果没有 figure，它便会调用 figure() 来创建一个，严格地说是创建一个 subplot

        调用顺序：
            默认情况下，
            matplotlib 会调用 gca() 来获取当前轴（axes）
            gca 调用 gcf() 来获取当前 figure，如果没有 figure，它便会调用 figure() 来创建一个，严格地说是创建一个 subplot

        图（Figures），参数如下：
            num	    1	figure的编号
            figsize	    figure.figsize	figure的大小(宽，高，单位英尺)
            dpi	    figure.dpi	每英尺内的像素点
            facecolor	figure.facecolor	背景色
            edgecolor	figure.edgecolor	边缘的颜色 background
            frameon	    True	是否有边界

        Subplots：
            通过 subplots ，你可以把其他坐标限定在常规坐标里。你需要指定行数和列数

        Axes：
            axes 非常类似于 subplots，但 axes 允许把 plots 放置在 figure 的任何位置。所以如果我们想把一个小的坐标放在大坐标里，我们应该用 axes

        Tick 定位器（Tick Locators）：
            被良好格式化的坐标轴是准备发布（publishing-ready）的 figures 的重要的一部分。Matplotlib 为坐标轴提供了一个完全可配置的系统。
            tick 定位器（tick locators）是用来指定ticks 应该在哪里出现，tick 格式化器（tick formatters）则是让 ticks 拥有你希望的外观。
            主要和次要的 ticks 可以单独指定位置和格式化。每个默认的次要 ticks 不会被显示，也就是说那里只会显示一个空的列表，因为它是 NullLocator（见下文）。
            主要定位器如下：
                    Class	        Description
                NullLocator     没有 ticks.
                IndexLocator    在每一个点的基础上绘制一个刻度。
                FixedLocator    Tick 的位置是固定的。
                LinearLocator   每隔一个间隔放置一个 Tick
                MultipleLocator     每隔单位间隔放置一个 Tick
                AutoLocator     Select no more than n intervals at nice locations.
                LogLocator      Determine the tick locations for log axes.
            所有的定位器都是从基类 matplotlib.ticker.Locator 派生

        Animation 制作动画
            在 matolotlib 中制作动画的最简单的方法是声明一个 FuncAnimation 对象，FuncAnimation 对象可以告知 matplotlib 哪个数字或哪个函数需要更新、
                使用什么函数来更新和每个帧之间的间隔
    """
    # New figure with white background
    fig = plt.figure(figsize=(6, 6), facecolor='white')

    # New axis over the whole figure, no frame and a 1:1 aspect ratio
    ax = fig.add_axes([0, 0, 1, 1], frameon=False, aspect=1)
    n = 50
    size_min = 50
    size_max = 50 * 50

    # Ring position
    P = np.random.uniform(0, 1, (n, 2))

    # Ring colors
    C = np.ones((n, 4)) * (0, 0, 0, 1)
    # Alpha color channel goes from 0 (transparent) to 1 (opaque)
    C[:, 3] = np.linspace(0, 1, n)

    # Ring sizes
    S = np.linspace(size_min, size_max, n)

    # Scatter plot
    scat = ax.scatter(P[:, 0], P[:, 1], s=S, lw=0.5,
                      edgecolors=C, facecolors='None')

    # Ensure limits are [0,1] and remove ticks
    ax.set_xlim(0, 1), ax.set_xticks([])
    ax.set_ylim(0, 1), ax.set_yticks([])

    def update(frame):
        global P, C, S

        # Every ring is made more transparent
        C[:,3] = np.maximum(0, C[:,3] - 1.0/n)

        # Each ring is made larger
        S += (size_max - size_min) / n

        # Reset ring specific ring (relative to frame number)
        i = frame % 50
        P[i] = np.random.uniform(0,1,2)
        S[i] = size_min
        C[i,3] = 1

        # Update scatter object
        scat.set_edgecolors(C)
        scat.set_sizes(S)
        scat.set_offsets(P)

        # Return the modified object
        return scat,

    animation = FuncAnimation(fig, update, interval=10, blit=True, frames=200)
    # ValueError: Cannot save animation: no writers are available. Please install ffmpeg to save animations. !!!
    animation.save('rain.gif', writer='imagemagick', fps=30, dpi=40)
    plt.show()


def f4():
    """
        地震图
    """
    pass


def f5():
    """
        填充图
    """
    n = 256
    X = np.linspace(-np.pi, np.pi, n, endpoint=True)
    Y = np.sin(2 * X)

    plt.axes([0.025, 0.025, 0.95, 0.95])

    plt.plot(X, Y + 1, color='blue', alpha=1.00)
    plt.fill_between(X, 1, Y + 1, color='blue', alpha=.25)

    plt.plot(X, Y - 1, color='blue', alpha=1.00)
    plt.fill_between(X, -1, Y - 1, (Y - 1) > -1, color='blue', alpha=.25)
    plt.fill_between(X, -1, Y - 1, (Y - 1) < -1, color='red', alpha=.25)

    plt.xlim(-np.pi, np.pi)
    #plt.xticks([])
    plt.ylim(-2.5, 2.5)
    #plt.yticks([])
    # savefig('../figures/plot_ex.png',dpi=48)
    plt.show()


def f6():
    """
        散点图
    """
    n = 1024
    X = np.random.normal(0, 1, n)
    Y = np.random.normal(0, 1, n)
    T = np.arctan2(Y, X)

    plt.axes([0.025, 0.025, 0.95, 0.95])
    plt.scatter(X, Y, s=75, c=T, alpha=.5)

    plt.xlim(-1.5, 1.5)
    #plt.xticks([])
    plt.ylim(-1.5, 1.5)
    #plt.yticks([])
    # savefig('../figures/scatter_ex.png',dpi=48)
    plt.show()


def f7():
    """
        条形图,  直方图
    """
    n = 12
    X = np.arange(n)
    Y1 = (1 - X / float(n)) * np.random.uniform(0.5, 1.0, n)
    Y2 = (1 - X / float(n)) * np.random.uniform(0.5, 1.0, n)

    plt.axes([0.025, 0.025, 0.95, 0.95])
    plt.bar(X, +Y1, facecolor='#9999ff', edgecolor='white')
    plt.bar(X, -Y2, facecolor='#ff9999', edgecolor='white')

    for x, y in zip(X, Y1):
        plt.text(x + 0.4, y + 0.05, '%.2f' % y, ha='center', va='bottom')

    for x, y in zip(X, Y2):
        plt.text(x + 0.4, -y - 0.05, '%.2f' % y, ha='center', va='top')

    plt.xlim(-.5, n)
    # plt.xticks([])
    plt.ylim(-1.25, +1.25)
    #plt.yticks([])

    # savefig('../figures/bar_ex.png', dpi=48)
    plt.show()


def f8():
    """
        轮廓图
    """

    def f(x, y):
        return (1 - x / 2 + x ** 5 + y ** 3) * np.exp(-x ** 2 - y ** 2)

    n = 256
    x = np.linspace(-3, 3, n)
    y = np.linspace(-3, 3, n)
    X, Y = np.meshgrid(x, y)

    #plt.axes([0.025, 0.025, 0.95, 0.95])

    plt.contourf(X, Y, f(X, Y), 8, alpha=.75, cmap=plt.cm.hot)
    C = plt.contour(X, Y, f(X, Y), 8, colors='black', linewidth=.5)
    plt.clabel(C, inline=1, fontsize=10)

    #plt.xticks([])
    #plt.yticks([])
    # savefig('../figures/contour_ex.png',dpi=48)
    plt.show()


def f9():
    """
        饼图
    """
    n = 20
    Z = np.ones(n)
    Z[-1] *= 2

    #plt.axes([0.025, 0.025, 0.95, 0.95])

    plt.pie(Z, explode=Z * .05, colors=['%f' % (i / float(n)) for i in range(n)],
            wedgeprops={"linewidth": 1, "edgecolor": "black"})
    plt.gca().set_aspect('equal')
    #plt.xticks([])
    #plt.yticks([])

    # savefig('../figures/pie_ex.png',dpi=48)
    plt.show()


def f10():
    """
        网格
    """
    #ax = plt.axes([0.025, 0.025, 0.95, 0.95])
    ax = plt.axes()

    ax.set_xlim(0, 4)
    ax.set_ylim(0, 3)
    ax.xaxis.set_major_locator(plt.MultipleLocator(1.0))
    ax.xaxis.set_minor_locator(plt.MultipleLocator(0.1))
    ax.yaxis.set_major_locator(plt.MultipleLocator(1.0))
    ax.yaxis.set_minor_locator(plt.MultipleLocator(0.1))
    ax.grid(which='major', axis='x', linewidth=0.75, linestyle='-', color='0.75')
    ax.grid(which='minor', axis='x', linewidth=0.25, linestyle='-', color='0.75')
    ax.grid(which='major', axis='y', linewidth=0.75, linestyle='-', color='0.75')
    ax.grid(which='minor', axis='y', linewidth=0.25, linestyle='-', color='0.75')
    #ax.set_xticklabels([])
    #ax.set_yticklabels([])

    # savefig('../figures/grid_ex.png',dpi=48)
    plt.show()


def f11():
    """
        子图，定义子图两种方法
            subplot(nrows,ncols,sharex,sharey,subplot_kw,**fig_kw)
    """
    fig = plt.figure()
    fig.subplots_adjust(bottom=0.025, left=0.025, top = 0.975, right=0.975)

    # 方法1
    plt.subplot(2,2,1)
    plt.xticks([])
    plt.yticks([])

    plt.subplot(2,2,2)
    plt.xticks([])
    plt.yticks([])

    plt.subplot(2,3,4)
    plt.xticks([])
    plt.yticks([])

    plt.subplot(2,3,5)
    plt.xticks([])
    plt.yticks([])

    plt.subplot(2,3,6)
    plt.xticks([])
    plt.yticks([])

    # 方法2
    fig, axes = plt.subplots(2, 2)
    #ax1 = axes[0, 0]
    ax1 = axes[0][0]
    #ax2 = axes[0, 1]
    ax2 = axes[0][1]
    #ax3 = axes[1, 0]
    ax3 = axes[1][0]
    #ax4 = axes[1, 1]
    ax4 = axes[1][1]
    x = np.arange(0, 100)
    # 作图1
    ax1.plot(x, x)
    # 作图2
    ax2.plot(x, -x)
    # 作图3
    ax3.plot(x, x ** 2)
    ax3.grid(color='r', linestyle='--', linewidth=1, alpha=0.3)
    # 作图4
    ax4.plot(x, np.log(x))

    # plt.savefig('../figures/multiplot_ex.png',dpi=48)


    plt.show()


def f12():
    """
        自定义子图布局排版
    """
    x = np.arange(0, 100)
    ax1 = plt.subplot2grid((3, 3), (0, 0), colspan=3)
    ax1.plot(x, np.log(x), linewidth=6, linestyle="-", label="log")
    ax1.legend(loc="upper left")

    ax2 = plt.subplot2grid((3, 3), (1, 0), colspan=2)
    ax2.plot(x, x ** 2)

    ax3 = plt.subplot2grid((3, 3), (1, 2), rowspan=2)
    ax4 = plt.subplot2grid((3, 3), (2, 0))
    ax5 = plt.subplot2grid((3, 3), (2, 1))
    plt.show()


def f13():
    """
        子图添加图例，即边角的小图标注释
    """
    ax1 = plt.subplot(2, 1, 1)
    x = np.arange(0, 100)
    ax1.plot(x, x ** 2, color="red", linewidth=5, linestyle="-", label="sine")
    # 添加边角的小图标注释
    ax1.legend(loc="upper right")

    ax2 = plt.subplot(2, 1, 2)
    ax2.plot(x, np.log(x), color="blue", linewidth=5, linestyle="-", label="cosine")
    # 添加边角的小图标注释
    ax2.legend(loc="upper left")
    plt.show()


def f14():
    """
        显示多图例，即一个figure显示多个图例
    """
    x = np.random.uniform(-1, 1, 4)
    y = np.random.uniform(-1, 1, 4)
    p1, = plt.plot([1, 2, 3])
    p2, = plt.plot([3, 2, 1])
    l1 = plt.legend([p2, p1], ["line 2", "line 1"], loc='upper left')

    p3 = plt.scatter(x[0:2], y[0:2], marker='D', color='r')
    p4 = plt.scatter(x[2:], y[2:], marker='D', color='g')
    # This removes l1 from the axes.
    plt.legend([p3, p4], ['label', 'label1'], loc='lower right', scatterpoints=1)
    # Add l1 as a separate artist to the axes
    plt.gca().add_artist(l1)
    plt.show()


    # 或者下面的方法，一个figure显示多个图例
    line1, = plt.plot([1, 2, 3], label="Line 1", linestyle='--')
    line2, = plt.plot([3, 2, 1], label="Line 2", linewidth=4)
    # 为第一个线条创建图例
    first_legend = plt.legend(handles=[line1], loc=1)
    # 手动将图例添加到当前轴域
    ax = plt.gca().add_artist(first_legend)
    # 为第二个线条创建另一个图例
    plt.legend(handles=[line2], loc=4)
    plt.show()


if __name__ == "__main__":
    #f1()
    #f2()
    #f3()
    #f5()
    #f6()
    #f7()
    #f8()
    #f9()
    #f10()
    #f11()
    f12()
    #f13()
    #f14()
