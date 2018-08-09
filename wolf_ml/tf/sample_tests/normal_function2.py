#coding=utf-8

import tensorflow as tf

def func1():
    """
    tf.shape()：
        获取变量的shape
    """
    t = tf.Variable(tf.random_normal([10, 100]))
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        print(tf.shape(t))
        print(sess.run(tf.shape(t)))

def func2():
    """
    tf.nn.softmax()：

    tf.argmax(input, dimension, name=None)
        dimension：dimension=0 按列找,dimension=1 按行找
    """
    y = tf.nn.softmax([1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0]) # tf.argmax(y, 0) 结果为10
    y = tf.nn.softmax([[1.5],[2.5],[3.5],[4.5],[3.5],[4.5],[7.5],[4.5],[9.5],[10.5]])
    y = tf.nn.softmax([[1.5,2.5],[3.5,4.5]])  # tf.argmax(y, 1) 结果为[1 1]
    with tf.Session() as sess:
        print(sess.run(y))
        print(sess.run(tf.argmax(y, 1)))

if __name__ == '__main__':
    #func1()

    func2()
