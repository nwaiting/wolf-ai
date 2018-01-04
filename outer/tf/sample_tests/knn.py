#coding=utf-8

import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data

def func_knn():
    minist = input_data.read_data_sets('./data', one_hot=True)
    X_train,Y_train = minist.train.next_batch(50000)
    X_test,Y_test = minist.test.next_batch(500)

    X_tr = tf.placeholder(tf.float32, shape=[None,784])
    X_te = tf.placeholder(tf.float32, shape=[784])

    #计算测试数据与训练数据L1范数大小（1表示从横轴进行降维）
    distance = tf.reduce_sum(tf.abs(tf.add(X_tr, tf.negative(X_te,))), reduction_indices=1)
    #求distance最小的下标
    predict = tf.argmin(distance, 0)

    accuracy = 0

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for i in range(len(X_test)):
            #knn算法 测试集和训练集对比 返回误差最小的下表
            nn_index = sess.run(predict, feed_dict={X_tr:X_train, X_te:X_test[i,:]})
            # #np.argmax  返回标签Y中最大数下标（既数值为1的下标），也就是该标签所对应的数字
            print("Test : ", i, " Prection : ", sess.run(tf.argmax(Y_train[nn_index])), " True class : ", sess.run(tf.argmax(Y_test[i])))

            #计算准确率
            if np.argmax(Y_train[nn_index]) == np.argmax(Y_test[i]):
                accuracy += 1/len(X_test)
        print("accuracy : ", accuracy)

if __name__ == '__main__':
    func_knn()
