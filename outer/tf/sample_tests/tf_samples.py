#coding=utf-8

"""
    tf相关总结的示例连接：
    http://blog.csdn.net/m0_37733057/article/details/72783996

    TensorFlow 示例
    https://github.com/aymericdamien/TensorFlow-Examples/blob/master/notebooks/2_BasicModels/linear_regression.ipynb
    https://github.com/aymericdamien/TensorFlow-Examples/blob/master/examples/2_BasicModels/linear_regression.py
"""

import tensorflow as tf

def main():
    """
    遍历tf.variable()变量
    """
    tensora = tf.Variable(tf.random_normal([10], dtype=tf.float32), dtype=tf.float32)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for i in zip(sess.run(tensora)):
            print(type(i), i, i[0])

if __name__ == '__main__':
    main()
