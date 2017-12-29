#coding=utf-8

"""
    可以画饼图、曲线、柱状图
    http://blog.csdn.net/wizardforcel/article/details/54407212
    含有三维图的示例
    http://blog.csdn.net/u011497262/article/details/52325705

    非常多示例 含有三维图
    http://blog.csdn.net/Notzuonotdied/article/details/77876080

    对LaTeX数学公式
    http://blog.csdn.net/ywjun0919/article/details/8692018

    含有动画
    http://blog.csdn.net/Notzuonotdied/article/details/77876080

    可以使用subplot()快速绘制包含多个子图的图表，它的调用形式如下：
    subplot(numRows, numCols, plotNum)
"""

import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np

def main():
    x_data = tf.Variable(tf.random_normal([100], dtype=tf.float32))
    y_data = tf.add(tf.multiply(x_data, 0.3) , 0.5)

    x_data = tf.Variable(tf.random_uniform([100], -5., 5., dtype=tf.float32))
    y_data = tf.add(tf.multiply(x_data, 0.233), 0.5)
    y_data = tf.add(y_data, tf.random_uniform([100], -0.2, 0.2, dtype=tf.float32))

    #x_data = np.linspace(-3, 3, 100)
    #y_data = np.sin(x_data) + np.random.uniform(-0.5, 0.5, 100)
    x_data = tf.Variable(tf.random_uniform([300], -5.0, 5.0, dtype=tf.float32), dtype=tf.float32, name='X')
    y_data = tf.add(tf.cos(x_data, name='Y'), tf.random_uniform([300], -1.0, 1.0, dtype=tf.float32))

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        # 创建一个图 设置分辨率等属性
        fig = plt.figure()
        """
        创建一个新的 1 * 1 的子图，接下来的图样绘制在其中的第 1 块（也是唯一的一块）
        subplot(1,1,1)
        子图：就是在一张figure里面生成多张子图
        add_subplot() 生成一张子图
        pyplot的方式中plt.subplot()参数和面向对象中的add_subplot()参数和含义都相同
        """
        ax = fig.add_subplot(1,1,1)
        #ax.scatter(sess.run(x_data), sess.run(y_data))
        #ax.scatter(x_data, y_data)
        #ax.plot(sess.run(x_data), sess.run(y_data), 'ro')
        # 绘制曲线，使用蓝色的、连续的、宽度为 1 （像素）的线条
        # plot(X, C, color="blue", linewidth=1.0, linestyle="-")
        plt.plot(sess.run(x_data), sess.run(y_data), 'ro')
        # 多个曲线画在一个图上
        #plt.legend()
        plt.show()

def main2():
    x = np.arange(0, 100)

    fig = plt.figure()

    ax1 = fig.add_subplot(221)
    ax1.plot(x, x)

    ax2 = fig.add_subplot(222)
    ax2.plot(x, -x)

    ax3 = fig.add_subplot(223)
    ax3.plot(x, x ** 2)

    ax4 = fig.add_subplot(224)
    ax4.plot(x, np.log(x))

    plt.show()

if __name__ == '__main__':
    main()
    #main2()
