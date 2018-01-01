#coding=utf-8

import sys
import random
import time
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

def main():
    """
    线性回归
    for data
    """
    #x_data = np.random.rand(100).astype(np.float32)
    #y_data = x_data * 0.1 + 0.3

    x_data = tf.Variable(tf.random_normal([100], dtype=tf.float32))
    y_data = tf.add(tf.multiply(x_data, 0.233), tf.add(5.377, tf.random_uniform([100], -0.5, 0.5, dtype=tf.float32)))

    """
    create module
    创建模型
    """
    Weights = tf.Variable(tf.random_uniform([1], -1., 1.))
    biases = tf.Variable(tf.zeros([1]))
    y = Weights * x_data + biases

    """
    cal loss
    """
    loss = tf.reduce_mean(tf.square(y - y_data))

    """
    基于梯度下降法的优化，步长为0.5
    """
    learn_rate = 0.01
    #optimizer = tf.train.GradientDescentOptimizer(learn_rate)
    optimizer = tf.train.ProximalGradientDescentOptimizer(learn_rate)
    """
    对损失函数优化
    """
    train = optimizer.minimize(loss=loss)

    """
    train
    """
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for step in range(1000):
            sess.run(train)
            if step % 20 == 0:
                print(step, sess.run(Weights), sess.run(biases))
        plt.plot(sess.run(x_data), sess.run(y_data), 'ro')
        plt.plot(sess.run(x_data), sess.run(tf.add(tf.multiply(x_data, Weights), biases)))
        plt.legend()
        plt.show()

def multi_linear_regression():
    """
    多项式回归
    """
    n_observation = 100
    x_s = tf.Variable(tf.random_uniform([n_observation], -3.0, 3.0, dtype=tf.float32), dtype=tf.float32, name='X')
    y_s = tf.add(tf.sin(x_s), tf.random_uniform([n_observation], -0.5, 0.5, dtype=tf.float32), name='Y')

    X = tf.placeholder(tf.float32)
    Y = tf.placeholder(tf.float32)

    W = tf.Variable(tf.random_normal([1], dtype=tf.float32), dtype=tf.float32)
    b = tf.Variable(tf.random_normal([1], dtype=tf.float32), dtype=tf.float32)

    y_pre = tf.add(tf.multiply(X, W), b)
    W_2 = tf.Variable(tf.random_normal([1], dtype=tf.float32), dtype=tf.float32)
    y_pre = tf.add(tf.multiply(tf.pow(X, 2), W_2), y_pre)
    W_3 = tf.Variable(tf.random_normal([1], dtype=tf.float32), dtype=tf.float32)
    y_pre = tf.add(tf.multiply(tf.pow(X, 3), W_3), y_pre)

    loss = tf.reduce_mean(tf.square(y_pre - Y))
    learn_rate = 0.01
    train = tf.train.GradientDescentOptimizer(learn_rate).minimize(loss)

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        # show source data
        #plt.scatter(sess.run(x_s), sess.run(y_s))
        #plt.show()

        for i in range(1000):
            total_loss = 0
            for tmpx, tmpy in zip(sess.run(x_s), sess.run(y_s)):
                _,l = sess.run([train, loss], feed_dict={X:tmpx, Y:tmpy})
                total_loss += l
            if i % 50 == 0:
                print('{0} {1} {2} {3} {4} {5}'.format(total_loss, total_loss/n_observation, sess.run(W), sess.run(W_2), sess.run(W_3), sess.run(b)))
        print('W {0}'.format(sess.run(W)))
        print('W2 {0}'.format(sess.run(W_2)))
        print('W3 {0}'.format(sess.run(W_3)))
        print('b {0}'.format(sess.run(b)))

        plt.plot(sess.run(x_s), sess.run(y_s), 'bo', label='real_data')
        first_add = tf.multiply(x_s, W)
        second_add = tf.multiply(tf.square(x_s), W_2)
        third_add = tf.multiply(tf.pow(x_s, 3), W_3)
        plt.plot(sess.run(x_s), sess.run(tf.add(tf.add(tf.add(first_add, second_add), third_add), b)), 'r', label='predict_data')
        plt.legend()
        plt.show()

def func_real(x):
    random.seed(int(time.time()))
    a0,a1,a2,a3,e = 0.1,-0.02,0.03,-0.04,0.05
    y = a0 + a1*x + a2*x*x + a3*x*x*x + e
    y += random.random()%5
    return y

def module(w, x, c):
    tmp = []
    for i in range(c):
        tmp.append(tf.multiply(tf.pow(x, i), w[i]))
    return tf.add_n(tmp)

def multi_linear_regression2():
    learn_rate = 0.01
    training_step = 50
    data_number = 100
    num_coeffs = 4
    source_data = np.linspace(-2, 3, data_number)
    x_data = tf.Variable(source_data, dtype=tf.float32)
    y_data = tf.Variable([func_real(x) for x in source_data], dtype=tf.float32)

    X = tf.placeholder(tf.float32)
    Y = tf.placeholder(tf.float32)

    W = tf.Variable([0.] * num_coeffs, dtype=tf.float32)
    y_pre = module(W, X, num_coeffs)

    loss = tf.reduce_mean(tf.square(y_pre - Y))
    train = tf.train.GradientDescentOptimizer(learn_rate).minimize(loss)

    #pre_x = np.linspace(-2, 3, data_number)
    pre_x = tf.Variable(tf.random_uniform([data_number], -2., 3., dtype=tf.float32), dtype=tf.float32)

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        for i in range(100):
            for m,n in zip(sess.run(x_data), sess.run(y_data)):
                _,l = sess.run([train, loss], feed_dict={X:m, Y:n})
                if i % training_step == 0:
                    print(l, sess.run(W))
        plt.plot(sess.run(x_data), sess.run(y_data), 'ro', label='real_data')
        pre_d = list()
        #pre_x = sorted(sess.run(pre_x))
        for i in range(num_coeffs):
            pre_d.append(tf.multiply(W[i], tf.pow(pre_x, i)))
        pre_d = tf.add_n(pre_d)
        plt.plot(sess.run(pre_x), sess.run(pre_d), 'g', label='predict_data')
        plt.legend()
        plt.show()


def multi_linear_regression3():
    learning_rate = 0.01
    training_epochs = 40
    rng = np.random.RandomState(1)

    def inner_fun(x):
        a0,a1,a2,a3,e = 0.1,-0.02,0.03,-0.04,0.05
        y = a0 + a1 * x + a2 * (x**2) + a3 * (x**3)+ e
        y += 0.03 * rng.rand(1)
        return y

    trX = np.linspace(-1, 1, 30)
    arrY = [inner_fun(x) for x in trX]
    num_coeffs = 4
    trY = np.array(arrY).reshape(-1,1)

    X = tf.placeholder("float")
    Y = tf.placeholder("float")

    def inner_model(X, w):
        terms = []
        for i in range(num_coeffs):
            term = tf.multiply(w[i], tf.pow(X, i))
            terms.append(term)
        return tf.add_n(terms)

    w = tf.Variable([0.] * num_coeffs, name="parameters")
    y_model = inner_model(X, w)

    cost = tf.reduce_sum(tf.square(Y-y_model))
    train_op = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

    with tf.Session() as sess :
        init = tf.global_variables_initializer()
        sess.run(init)

        for epoch in range(training_epochs):
            for (x, y) in zip(trX, trY):
                sess.run(train_op, feed_dict={X: x, Y: y})

        w_val = sess.run(w)
        print(w_val)

    plt.figure()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.title('polynomial regression(tensorflow)')
    plt.scatter(trX, trY)
    trX2 = np.linspace(-1, 2, 100)
    trY2 = 0
    for i in range(num_coeffs):
        trY2 += w_val[i] * np.power(trX2, i)
    plt.plot(trX2, trY2, 'r-')
    plt.show()

if __name__ == '__main__':
    #main()
    #multi_linear_regression()
    multi_linear_regression2()
    #multi_linear_regression3()
