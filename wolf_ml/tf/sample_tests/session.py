#coding=utf8

import tensorflow as tf

def main():
    tensor_a = tf.constant('hello')
    """
    1、
    """
    sess = tf.Session()
    sess.close()

    """
    2、
    """
    with tf.Session() as sess:
        print(sess.run(tensor_a))

    """
    3、
    """
    sess = tf.Session()
    with sess.as_default():
        print(sess.run(tensor_a))

def func_graph():
    """
    在tensorflow中始终存在一个默认的图，
    """
    g1 = tf.Graph()
    with g1.as_default():
        c1 = tf.constant('first default')

    with tf.Graph().as_default() as g2:
        c2 = tf.constant('second default')

    with tf.Session(graph=g1) as sess1:
        print(sess1.run(c1))

    with tf.Session(graph=g2) as sess2:
        print(sess2.run(c2))

if __name__ == "__main__":
    #main()
    func_graph()
