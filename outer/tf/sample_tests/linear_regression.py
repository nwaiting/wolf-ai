#coding=utf-8

import sys
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

import tensorflow as tf
import numpy as np

def main():
    """
    for data
    """
    #x_data = np.random.rand(100).astype(np.float32)
    #y_data = x_data * 0.1 + 0.3

    x_data = tf.Variable(tf.random_normal([100], dtype=tf.float32))
    y_data = tf.add(tf.multiply(x_data, 0.233), 0.377)

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

    optimizer = tf.train.GradientDescentOptimizer(0.5)
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

if __name__ == '__main__':
    main()
