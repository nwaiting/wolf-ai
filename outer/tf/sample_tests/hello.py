#coding=utf8
import tensorflow as tf
import numpy as np

def main():
    x_data = np.float32(np.random.rand(2, 100))
    y_data = np.dot([0.1,0.2], x_data) + 0.3

    # 构造线性模型
    b = tf.Variable(tf.zeros([1]))
    W = tf.Variable(tf.random_uniform([1,2], -1.0, 1.0))
    y = tf.matmul(W, x_data) + b

    #最小方差
    loss = tf.reduce_mean(tf.square(y - y_data))
    optimizer = tf.train.GradientDescentOptimizer(0.5)
    train = optimizer.minimize(loss)

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
