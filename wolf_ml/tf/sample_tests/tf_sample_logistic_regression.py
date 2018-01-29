#coding=utf-8

from __future__ import print_function
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import os
data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
minist = input_data.read_data_sets(data_path, one_hot=True)

def logistic_func1():
    learn_rate = 0.01
    epoch_times = 500
    display_step = 20

    #定义批梯度下降次数，每100张图计算一次梯度
    batch_size = 100

    X = tf.placeholder(tf.float32, shape=[None,784])
    Y = tf.placeholder(tf.float32, shape=[None, 10])

    W = tf.Variable(tf.zeros([784,10]))
    b = tf.Variable(tf.zeros([10]))

    # 返回一个10维矩阵
    # 注意X,W前后顺序 [None,784]*[784,10]=[None,10]
    pred = tf.nn.softmax(tf.matmul(X, W)+b)

    '''
    tf.reduce_sum(-Y * tf.log(pred), 1) 返回每个实例的交叉熵(向量)，1代表水平方向求和
    tf.reduce_mean() 返回所有交叉熵的平均值(实数)
    '''
    loss = tf.reduce_mean(tf.reduce_sum(-Y * tf.log(pred),reduction_indices=1))

    optimizer = tf.train.GradientDescentOptimizer(learn_rate).minimize(loss=loss)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for epoch in range(epoch_times):
            #批量梯度下降 返回总批量次数(55000/100=550)
            batch_number =int(minist.train.num_examples/batch_size)
            train_cost = 0
            for i in range(batch_number):
                batch_Xs, batch_Ys = minist.train.next_batch(batch_size)
                _,batch_cost = sess.run([optimizer,loss], feed_dict={X:batch_Xs,Y:batch_Ys})
                train_cost += batch_cost/batch_number
            if (epoch + 1) % display_step == 0:
                print('epoch : %04d '%(epoch+1), 'train_cost : {:9f}'.format(train_cost))
        print('Optimization finished')

        # tf.arg_max(pred,1):得到向量中最大数的下标，1代表水平方向
        # tf.equal():返回布尔值，相等返回1，否则0
        # 最后返回大小[none,1]的向量，1所在位置为布尔类型数据
        correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(Y, 1))
        # tf.cast():将布尔型向量转换成浮点型向量
        # tf.reduce_mean():求所有数的均值
        # 返回正确率：也就是所有为1的数目占所有数目的比例
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        #输入正确率
        print("train accuracy : ", sess.run(accuracy, feed_dict={X:minist.train.images, Y:minist.train.labels}))
        print("test accuracy : ", sess.run(accuracy, feed_dict={X:minist.test.images, Y:minist.test.labels}))

def func2():
    # 对数几率回归
    W = tf.Variable(tf.zeros([5,1]),dtype=tf.float32, name='weigths')
    b = tf.Variable(0., dtype=tf.float32, name='biasis')
    Y = tf.Variable()

    #输入合并
    combine_inputs = tf.add(tf.matmul(X, W), b)
    loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=combine_inputs, labels=Y))

    learn_rate = 0.01
    optimizer = tf.train.GradientDescentOptimizer(learn_rate).minimize(loss)

    #评估训练模型
    #调用概率分布函数
    tfsig = tf.sigmoid(tf.add(tf.matmul(X,W),b))
    predicted = tf.cast(tfsig>0.5, tf.float32)
    result = tf.reduce_mean(tf.cast(tf.equal(predicted, Y), tf.float32))

def func3():
    learning_rate = 0.01
    training_epochs = 25
    batch_size = 100
    display_step = 1
    X = tf.placeholder(tf.float32, shape=[None, 784])
    Y = tf.placeholder(tf.float32, shape=[None, 10])

    # set model weigths
    W = tf.Variable(tf.zeros([784, 10]))
    b = tf.Variable(tf.zeros([10]))

    # construct model
    prediction = tf.nn.softmax(tf.add(tf.matmul(X, W), b)) #softmax

    # loss
    loss = tf.reduce_mean(-tf.reduce_sum(Y * tf.log(prediction), reduction_indices=1))

    #optimizer
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(loss=loss)

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for epoch in range(training_epochs):
            avg_cost = 0
            total_batch = int(minist.train.num_examples/batch_size)
            for i in range(total_batch):
                batch_x, batch_y = minist.train.next_batch(batch_size)
                _, c = sess.run([optimizer, loss], feed_dict={X:batch_x, Y:batch_y})
                avg_cost += c / total_batch
            if (epoch+1) % display_step == 0:
                print('epoch {0} cost {1}'.format(epoch+1, avg_cost))
        print('optimizer done')
        correct_prediction = tf.equal(tf.argmax(prediction, 1), tf.argmax(Y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        print('accuracy {0}'.format(accuracy.eval({X:minist.test.images, Y:minist.test.labels})))

if __name__ == '__main__':
    #logistic_func1()
    func3()
