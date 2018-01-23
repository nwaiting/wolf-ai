#coding=utf-8

"""
    tf相关总结的示例连接：
    http://blog.csdn.net/m0_37733057/article/details/72783996

    TensorFlow 示例
    https://github.com/aymericdamien/TensorFlow-Examples/blob/master/notebooks/2_BasicModels/linear_regression.ipynb
    https://github.com/aymericdamien/TensorFlow-Examples/blob/master/examples/2_BasicModels/linear_regression.py
"""

import tensorflow as tf
import numpy as np

def main():
    """
    遍历tf.variable()变量
    """
    tensora = tf.Variable(tf.random_normal([10], dtype=tf.float32), dtype=tf.float32)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for i in zip(sess.run(tensora)):
            print(type(i), i, i[0])

def func1():
    """
    embedding_lookup 选取一个张量里面索引对应的元素
    tf.nn.embedding_lookup(tensor, id)：tensor输入张量，id张量对于的索引，就是返回tensor中的第id行
    """
    a = [[0.1, 0.2, 0.3], [1.1, 1.2, 1.3], [2.1, 2.2, 2.3], [3.1, 3.2, 3.3], [4.1, 4.2, 4.3]]
    a = np.asarray(a)
    idx1 = tf.Variable([0, 2, 3, 1], tf.int32)
    idx2 = tf.Variable([[0, 2, 3, 1], [4, 0, 2, 2]], tf.int32)
    out1 = tf.nn.embedding_lookup(a, idx1)
    out2 = tf.nn.embedding_lookup(a, idx2)
    init = tf.global_variables_initializer()

    with tf.Session() as sess:
        sess.run(init)
        print (sess.run(out1))
        print (out1)
        print ('==================')
        print (sess.run(out2))
        print (out2)

def func2():
    """
    Tensorflow实现了两种常用与word2vec的loss，sampled softmax和NCE，
    两个方法的目标是在分类目标数量太大时，采用估算的方法简化softmax的计算
    sampled softmax：
        把多分类问题转化成二分类。之前计算softmax的时候class数量太大，NCE索性就把分类缩减为二分类问题。
        之前的问题是计算某个类的归一化概率是多少，二分类的问题是input和label正确匹配的概率是多少。二分类问题群众喜闻乐见，直接上logistic regression估算一下概率

    NCE:
        Sampled softmax则是只抽取一部分样本计算softmax。这个想法也很好理解，训练的时候我不需要特别精准的softmax归一化概率，我只需要一个粗略值做back propoagation就好了
    """
    tf.nn.nce_loss()
    tf.nn.sampled_softmax_loss()

if __name__ == '__main__':
    #main()
    #func1()
    func2()
