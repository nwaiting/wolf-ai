#coding=utf8
import tensorflow as tf
import numpy as np

"""
"""

def main():
    #二维数据 100个数
    x_data = np.float32(np.random.rand(2, 100))
    # 类似二元回归问题np.dot([权重参数,权重参数],x) + 偏置
    # 类似 W转置 * X + b
    y_data = np.dot([0.1,0.2], x_data) + 0.3

    # 1、 inference() 建立好图表 满足促使神经网络向前反馈并做出预测的要求
    # 构造线性模型 建模过程
    # 初始化
    b = tf.Variable(tf.zeros([1]))
    # 1*2 matrix
    W = tf.Variable(tf.random_uniform([1,2], -1.0, 1.0))
    """
    自定义初始化：
        tf.random_uniform([1,2], -1.0, 1.0, stddev=0.35)
        w2 = tf.Variable(W.initialized_value())
        w3 = tf.Variable(W.initialized_value() * 0.3)
    """
    # 矩阵相乘
    y = tf.matmul(W, x_data) + b

    #2、loss() 往inference图表中添加生成损失所需要的操作
    #最小方差 均方差
    loss = tf.reduce_mean(tf.square(y - y_data))
    #学习率
    #3、往损失图表中添加计算并应用梯度所需操作
    optimizer = tf.train.GradientDescentOptimizer(0.5)
    train = optimizer.minimize(loss)

    """
    运算核 是一个运算操作在某个具体的硬件(在CPU或者GPU中)的实现
    可以注册机制加入新的运算操作或者为已有的运算操作添加新的计算核
    """

    # 定义biases为一维的零
    biases = tf.Variable(tf.zeros([1]))

    #初始化变量
    init = tf.initialize_all_variables()

    #启动图
    sess = tf.Session()
    sess.run(init)

    #拟合平面
    for step in xrange(0, 200):
        sess.run(train)
        if step % 20 == 0:
            print step, sess.run(W), sess.run(b)

if __name__ == "__main__":
    main()
