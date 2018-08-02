#coding=utf-8
import os
import numpy as np
import tensorflow as tf
from tensorflow.contrib import rnn
from tensorflow.examples.tutorials.mnist import input_data
import matplotlib.pyplot as plt

"""
    设置日志
"""
tf.logging.set_verbosity(tf.logging.INFO)

"""
'''
    初始化训练变量
'''

data_path = 'D:\\opensource\\scrapy-work\\wolf_ml\\tf\\sample_tests\\data'
mnist = input_data.read_data_sets(data_path, one_hot=True)
#file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mnist.npz')
#(x_train,y_train),(x_test,y_test) = tf.keras.datasets.mnist.load_data(file_name)

learning_rate = 0.001
training_step = 10000
batch_size = 128
display_step = 200

num_input = 28  # mnist data input (image 28*28)
timesteps = 28  # timesteps
num_hidden = 128 # hidden layer number of features
num_classes = 10 # total classes (0-9 digits)

def BiRNN(x, weights, biases):
    # get a list of timesteps tensors of shape (batch_size, num_input)
    x = tf.unstack(x, timesteps, 1)

    lstm_fw_cell = rnn.BasicLSTMCell(num_hidden, forget_bias=1.0)
    lstm_bw_cell = rnn.BasicLSTMCell(num_hidden, forget_bias=1.0)

    outputs,_,_ = rnn.static_bidirectional_rnn(lstm_fw_cell, lstm_bw_cell, x, dtype=tf.float32)

    return tf.matmul(outputs[-1], weights['out']) + biases['out']

def main():
    #input
    X = tf.placeholder(tf.float32, [None, timesteps, num_input])
    y = tf.placeholder(tf.float32, [None, num_classes])

    weights = {'out':tf.Variable(tf.random_normal([2*num_hidden, num_classes]))}
    biases = {'out':tf.Variable(tf.random_normal([num_classes]))}

    logits = BiRNN(X, weights, biases)
    prediction = tf.nn.softmax(logits=logits)

    loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=y))
    train_op = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(loss_op)

    correct_pred = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    init = tf.global_variables_initializer()

    with tf.Session() as sess:
        sess.run(init)
        for step in range(training_step):
            batch_x, batch_y = mnist.train.next_batch(batch_size)
            batch_x = batch_x.reshape((batch_size, timesteps, num_input))
            sess.run(train_op, feed_dict={X:batch_x, y:batch_y})
            if step%display_step == 0:
                loss, acc = sess.run([loss_op,accuracy], feed_dict={X:batch_x, y:batch_y})
                print('step {0} loss {1} accuracy {2}'.format(step, loss, acc))
        print('optimization finished')

        test_len = 128
        test_data = mnist.test.images[:test_len].reshape((-1, timesteps, num_input))
        test_label = mnist.test.labels[:test_len]
        print('test accuracy {0}'.format(sess.run(accuracy, feed_dict={X:test_data, y:test_label})))
"""


class BiLSTM(object):
    def __init__(self):
        self.learning_rate = 0.001
        #迭代训练时候总共的样本数
        self.training_step = 1000000
        #每次训练的样本大小
        self.batch_size = 128
        #显示的样本
        self.display_step = 200

        #timesteps * num_input 就是一张图，把每一行拆到每个timesteps上
        self.num_input = 28  # mnist data input (image 28*28)
        self.timesteps = 28  # timesteps

        #隐层大小
        self.num_hidden = 128 # hidden layer number of features
        self.num_classes = 10 # total classes (0-9 digits)

        self.test_len = 128

        #graph input，None表示这一维大小不确定
        self.X = tf.placeholder(tf.float32, [None, self.timesteps, self.num_input])
        self.y = tf.placeholder(tf.float32, [None, self.num_classes])

        self.mnist = None
        self.train_op = None
        self.accuracy = None
        self.loss_op = None
        self.load_data()

    def load_data(self):
        data_path = 'D:\\opensource\\scrapy-work\\wolf_ml\\tf\\sample_tests\\data'
        self.mnist = input_data.read_data_sets(data_path, one_hot=True)

    def BiRNN(self, x, weights, biases):
        #改变张量的维度
        # Prepare data shape to match `rnn` function requirements
        # Current data input shape: (batch_size, timesteps, n_input)
        # Required shape: 'timesteps' tensors list of shape (batch_size, num_input)
        # 变成了 timesteps * (batch_size, num_input)
        x = tf.unstack(x, self.timesteps, 1)

        lstm_fw_cell = rnn.BasicLSTMCell(self.num_hidden, forget_bias=1.0)
        lstm_bw_cell = rnn.BasicLSTMCell(self.num_hidden, forget_bias=1.0)

        outputs,output_state_fw,output_state_bw = rnn.static_bidirectional_rnn(lstm_fw_cell, lstm_bw_cell, x, dtype=tf.float32)

        return tf.matmul(outputs[-1], weights) + biases

    def generator_net(self):
        weights = tf.Variable(tf.random_normal([2*self.num_hidden, self.num_classes]))
        biases = tf.Variable(tf.random_normal([self.num_classes]))

        logits = self.BiRNN(self.X, weights, biases)
        prediction = tf.nn.softmax(logits=logits)

        #我们使用最简单的最小均方误差(MSE)作为损失函数
        #reduce_mean就是对所有数值（没有指定哪一维）求均值
        self.loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=self.y))
        self.train_op = tf.train.GradientDescentOptimizer(learning_rate=self.learning_rate).minimize(self.loss_op)

        # evaluate model
        correct_pred = tf.equal(tf.argmax(prediction, 1), tf.argmax(self.y, 1))
        self.accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    def train(self):
        # 构造网络
        self.generator_net()

        init = tf.global_variables_initializer()

        with tf.Session() as sess:
            sess.run(init)
            train_result = []
            for step in range(0,self.training_step,self.batch_size):
                batch_x, batch_y = self.mnist.train.next_batch(self.batch_size)
                print('batch_y ', batch_y)
                batch_x = batch_x.reshape((self.batch_size, self.timesteps, self.num_input))
                sess.run(self.train_op, feed_dict={self.X:batch_x, self.y:batch_y})
                if step%self.display_step == 0:
                    loss, acc = sess.run([self.loss_op,self.accuracy], feed_dict={self.X:batch_x, self.y:batch_y})
                    print('step {0} loss {1} accuracy {2}'.format(step, loss, acc))
                    train_result.append((step, loss, acc))
            print('optimization finished')

            #plt.plot([i[0] for i in train_result], [i[1] for i in train_result])
            plt.plot([i[0] for i in train_result], [i[2] for i in train_result])
            plt.show()

            test_data = self.mnist.test.images[:self.test_len].reshape((-1, self.timesteps, self.num_input))
            test_label = self.mnist.test.labels[:self.test_len]
            print('test accuracy {0}'.format(sess.run(self.accuracy, feed_dict={self.X:test_data, self.y:test_label})))


if __name__ == '__main__':
    #main()

    bilstm = BiLSTM()
    bilstm.train()
