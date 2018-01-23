#coding=utf-8

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from random import random

"""
from tensorflow.contrib.factorization import KMeans,KMeansClustering
from tensorflow.contrib.bayesflow
from tensorflow.contrib.boosted_trees
"""

#为了使图中出现中文
from pylab import mpl
mpl.rcParams['font.sans-serif'] =['SimHei']

def main():
    iris = datasets.load_iris()
    x_vals = np.array([[x[0], x[3]] for x in iris.data])
    y_vals = np.array([1 if y == 0 else -1 for y in iris.target])

    #测试集和训练集的比例我们设置为8:2
    train_indices = np.random.choice(len(x_vals), round(len(x_vals)*0.8), replace=False)
    test_indices = np.array(list(set(range(len(x_vals))) - set(train_indices)))
    #样本
    x_vals_train = x_vals[train_indices]
    x_vals_test = x_vals[test_indices]
    #标签
    y_vals_train = y_vals[train_indices]
    y_vals_test = y_vals[test_indices]

    batch_size = 100
    #初始化feed_dict
    # shape：数据形状。默认是None，就是一维值，也可以是多维，比如[2,3], [None, 3]表示列是3，行不定
    x_data = tf.placeholder(tf.float32, shape=[None, 2])
    y_target = tf.placeholder(tf.float32, shape=[None, 1])

    #创建变量
    W = tf.Variable(tf.random_normal(shape=[2,1], dtype=tf.float32), dtype=tf.float32)
    b = tf.Variable(tf.random_normal(shape=[1,1], dtype=tf.float32), dtype=tf.float32)

    #定义线性模型 y = wx + b
    model_output = tf.subtract(tf.matmul(x_data, W),b)

    #L2范数
    l2_norm = tf.reduce_sum(tf.square(W))

    # loss = max(0, 1-pred*actual) + alpha * L2_norm(A)^2
    """
    接下来定义可以优化的损失函数。在SVM中，我们利用Hinge Loss作为损失函数。计算结果为model_output，损失函数定义为 1/n ∑max(0,1-y_i (ωx_i+b)) +α∥ω∥^2 ,其中， α 为软正则化系数，在这里，我们设置为0.1
    """
    #软正则化参数
    alpha = tf.constant([0.01])
    classification_term = tf.reduce_mean(tf.maximum(0., tf.subtract(1., tf.multiply(model_output, y_target))))
    loss = tf.add(classification_term, tf.multiply(alpha, l2_norm))

    learn_rate = 0.01
    optimizer = tf.train.GradientDescentOptimizer(learn_rate).minimize(loss=loss)

    saver = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        #训练误差 训练准确率 测试准确率
        loss_vec = []
        train_accuracy = []
        test_accuracy = []
        for i in range(2000):
            rand_index = np.random.choice(len(x_vals_train), size=batch_size)
            rand_x = x_vals_train[rand_index]
            rand_y = np.transpose([y_vals_train[rand_index]])
            sess.run(optimizer, feed_dict={x_data:rand_x, y_target:rand_y})
        saver.save(sess,'./outer/tf/sample_tests/data/svm_model.ckpt')
        [[a1], [a2]] = sess.run(W)
        [[b1]] = sess.run(b)
        slope = -a2/a1
        y_intercept = b1/a1
        best_fit = []
        x1_vals = [d[1] for d in x_vals]
        for i in x1_vals:
            best_fit.append(slope * i + y_intercept)

        setosa_x = [d[1] for i,d in enumerate(x_vals) if y_vals[i] == 1]
        setosa_y = [d[0] for i,d in enumerate(x_vals) if y_vals[i] == 1]
        not_setosa_x = [d[1] for i,d in enumerate(x_vals) if y_vals[i] == -1]
        not_setosa_y = [d[0] for i,d in enumerate(x_vals) if y_vals[i] == -1]

        plt.plot(setosa_x, setosa_y, 'o', label='I. setosa')
        plt.plot(not_setosa_x, not_setosa_y, 'x', label='Non-setosa')
        plt.plot(x1_vals, best_fit, 'r-', label='Linear Separator', linewidth=3)
        plt.ylim([0, 10])
        # plt.legend(['损失','训练精确度','测试精确度'])
        plt.legend(loc='lower right')
        plt.title('Sepal Length vs Pedal Width')
        plt.xlabel('Pedal Width')
        plt.ylabel('Sepal Length')
        plt.show()

def func2():
    import time
    np.random.seed(int(time.time()))
    tf.set_random_seed(int(time.time()))
    iris = datasets.load_iris()
    x_values = iris.data
    y_values = np.array([1 if y==0 else -1 for y in iris.target])

    #划分训练集和测试机
    train_indices = np.random.choice(len(x_values), round(len(x_values)*0.8), replace=False)
    test_indices = np.array(list(set(range(len(x_values))) - set(train_indices)))

    x_values_train = x_values[train_indices]
    y_values_train = y_values[train_indices]
    x_values_test = x_values[test_indices]
    y_values_test = y_values[test_indices]

    #批训练
    batch_size = 100
    x_data = tf.placeholder(tf.float32, shape=[None, 4])
    y_data = tf.placeholder(tf.float32, shape=[None, 1])
    W = tf.Variable(tf.random_normal(shape=[4,1]))
    b = tf.Variable(tf.random_normal(shape=[1,1]))

    #定义损失函数 Hinge Loss作为损失函数
    model_output = tf.add(tf.matmul(x_data, W), b)
    l2_norm = tf.reduce_sum(tf.square(W))
    #软正则化
    alpha = tf.constant([0.1])
    #损失函数
    classification_term = tf.reduce_mean(tf.maximum(0., 1. - model_output * y_data))
    loss = classification_term + alpha * l2_norm

    #输出
    prediction = tf.sign(model_output)
    accuracy = tf.reduce_mean(tf.cast(tf.equal(prediction, y_data), tf.float32))
    learn_rate = 0.01
    optimizer = tf.train.GradientDescentOptimizer(learn_rate).minimize(loss=loss)

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        loss_vector = []
        train_accuracy = []
        test_accuracy = []
        for i in range(100):
            rand_index = np.random.choice(len(x_values_train), size=batch_size)
            rand_x = x_values_train[rand_index]
            rand_y = np.transpose([y_values_train[rand_index]])
            _,temp_loss = sess.run([optimizer, loss], feed_dict={x_data:rand_x, y_data:rand_y})
            loss_vector.append(temp_loss)
            train_acc_temp = sess.run(accuracy, feed_dict={x_data:x_values_train, y_data:np.transpose([y_values_train])})
            train_accuracy.append(train_acc_temp)
            test_acc_temp = sess.run(accuracy, feed_dict={x_data:x_values_test, y_data:np.transpose([y_values_test])})
            test_accuracy.append(test_acc_temp)
            if i%50 == 0:
                print('step {0}, W = {1}, b = {2}, loss = {3}'.format(i, sess.run(W), sess.run(b), temp_loss))

        plt.plot(loss_vector)
        plt.plot(train_accuracy)
        plt.plot(test_accuracy)
        plt.legend(['损失', '训练误差', '测试误差'])
        #设置y轴的范围
        plt.ylim(0., 1.)
        plt.show()

if __name__ == '__main__':
    #main()
    func2()
