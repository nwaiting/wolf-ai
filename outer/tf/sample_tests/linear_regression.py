#coding=utf-8

import sys
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

import tensorflow as tf
import numpy as np

def main():
    """
    线性回归
    for data
    """
    #x_data = np.random.rand(100).astype(np.float32)
    #y_data = x_data * 0.1 + 0.3

    x_data = tf.Variable(tf.random_normal([100], dtype=tf.float32))
    y_data = tf.add(tf.multiply(x_data, 0.233), tf.add(5.377, tf.random_uniform([100], -1.0, 1.0, dtype=tf.float32)))

    """
    create module
    """
    Weights = tf.Variable(tf.random_uniform([1], -1., 1.))
    biases = tf.Variable(tf.zeros([1]))
    y = Weights * x_data + biases

    """
    cal loss
    """
    loss = tf.reduce_mean(tf.square(y - y_data))

    learn_rate = 0.5
    #optimizer = tf.train.GradientDescentOptimizer(learn_rate)
    optimizer = tf.train.ProximalGradientDescentOptimizer(learn_rate)
    train = optimizer.minimize(loss=loss)

    """
    train
    """
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for step in range(200):
            sess.run(train)
            if step % 20 == 0:
                print(step, sess.run(Weights), sess.run(biases))

def multi_linear_regression():
    """
    多项式回归
    """
    n_observation = 300
    x_s = tf.Variable(tf.random_uniform([n_observation], -5.0, 5.0, dtype=tf.float32), dtype=tf.float32, name='X')
    y_s = tf.add(tf.cos(x_s), tf.random_uniform([n_observation], -1.0, 1.0, dtype=tf.float32), name='Y')

    X = tf.placeholder(tf.float32)
    Y = tf.placeholder(tf.float32)

    W = tf.Variable(tf.random_normal([1], dtype=tf.float32), dtype=tf.float32)
    b = tf.Variable(tf.random_normal([1], dtype=tf.float32), dtype=tf.float32)

    y_pre = tf.add(tf.multiply(X, W), b)
    W_2 = tf.Variable(tf.random_normal([1], dtype=tf.float32), dtype=tf.float32)
    y_pre = tf.add(tf.multiply(tf.pow(X, 2), W_2), y_pre)
    W_3 = tf.Variable(tf.random_normal([1], dtype=tf.float32), dtype=tf.float32)
    y_pre = tf.add(tf.multiply(tf.pow(X, 2), W_3), y_pre)

    loss = tf.reduce_mean(tf.square(y_pre - Y))
    learn_rate = 0.03
    train = tf.train.GradientDescentOptimizer(learn_rate).minimize(loss)

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for i in range(1000):
            total_loss = 0
            for tmpx, tmpy in zip(sess.run(x_s), sess.run(y_s)):
                _,l = sess.run([train, loss], feed_dict={X:tmpx, Y:tmpy})
                print('======== ', l)
                total_loss += l
            if i % 50 == 0:
                print(total_loss, total_loss/n_observation)

if __name__ == '__main__':
    #main()
    multi_linear_regression()
