#coding=utf-8

import tensorflow as tf
import tensorflow.contrib.layers.python.layers.encoders

"""
    使用rnn（用gru或者lstm）完成文本分类
"""
def rnn_model(features, target):
    #先进行序列 [n_words,EMBEDDING_SIZE]
    tf.contrib.layers.embed_sequence(features, vocab_size=n_words, embed_dim=EMBEDDING_SIZE, scope='word')

    #将每一个词变成一个tensor[batch_size,EMBEDDING_SIZE]
    word_list = tf.unstack(word_vectors, axis=1)

    #create gated recurrent unit cell
    cell = tf.contrib.rnn.GRUCell(EMBEDDING_SIZE)
    cell = tf.contrib.rnn.LSTMCell(EMBEDDING_SIZE)

    #create an unrolled recurrent Neural Network to length of MAX_DOCUMENT_LENGTH and passes word_list as inputs for each unit
    _,encoding= tf.contrib.rnn.static_rnn(cell, word_list, dtype=tf.float32)

    target = tf.one_hot(target, 15, 1, 0)
    logits = tf.contrib.layers.fully_connected(encoding, 15, activation_fn=None)
    loss = tf.contrib.losses.softmax_cross_entropy(logits, target)

    train_op = tf.contrib.layers.optimize_loss(loss, tf.contrib.framework.get_global_step(), optimizer='Adam', learning_rate=0.01)


"""
    tensorflow的多层lstm流程
"""

"""
    1、初始化，设置模型的用到的超参数
"""
import numpy as np
from tensorflow.contrib import rnn
from tensorflow.examples.tutorials.mnist import input_data
#设置GPU按需增长
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)

#导入数据
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

#设置超参数
lr = 1e-3

#在训练的时候要用不同的batch_size
batch_size = tf.placeholder(tf.int32, [])
keep_prob = tf.placeholder(tf.float32, [])

#在每个时刻的输入特征是28维，就是每个时刻输入一行，一行有28个像素
input_size = 28
#时序持续长度为28，即没做一次预测，需要先输入28行
timestep_size = 28
#每个隐含层的节点数
hidden_size = 256
#lstm layer的层数
layer_num = 2
#最后输出分类类别的数量，如果是回归预测的话应该是1
class_num = 10

X = tf.placeholder(tf.float32, [None, 784])
y = tf.placeholder(tf.float32, [None, class_num])

"""
    2、开始搭建LSTM模型，和普通RNN模型一样
"""
#1、RNN的输入shape=(batch_size, timestep_size, input_size)
#还原成[28,28]
X = tf.reshape(X, [-1,, 28, 28])

#2、定义一层LSTM_cell,只需要说明hidden_size，它会自动匹配输入的X的维度
lstm_cell = rnn.BasicLSTMCell(num_units=hidden_size, forget_bias=1.0, state_is_tuple=True)

#3、添加dropout layer，一般只设置output_keep_prob
lstm_cell = rnn.DropoutWrapper(cell=lstm_cell, input_keep_prob=1.0, output_keep_prob=keep_prob)

#4、通过MultiRNNCell来实现多层LSTM
mlstm_cell = rnn.MultiRNNCell([lstm_cell] * layer_num, state_is_tuple=True)

#5、使用全零来初始化state
init_state = mlstm_cell.zero_state(batch_size=batch_size, dtype=tf.float32)

#6、方法1：调用dynamic_rnn()来使构建的网络开始运行
# 当 time_major=False时，outputs.shape = [batch_size, timestep_size, hidden_size]
# 所以，可以取 h_state = outputs[:, -1, :] 作为最后输出
# state_shape = [layer_num, 2, batch_size, hidden_size]
# 或者可以取h_state = state[-1][1] 作为最后输出
# 最后输出维度是 [batch_size, hidden_size]
outputs,state = tf.nn.dynamic_rnn(mlstm_cell, inputs=X, initial_state=init_state, time_major=False)
h_state = outputs[:, -1, :]
#或者
h_state = state[-1][1]

#实现步骤6中的函数
#按时间步展开计算
outputs = list()
state = init_state
with tf.variable_scope('RNN'):
    for timestep in range(timestep_size):
        if timestep > 0:
            tf.get_variable_scope().reuse_variables()
        #这里的state保存了每一层lstm的状态
        (cell_output,state) = mlstm_cell(X[:, timestep, :], state=state)
        outputs.append(cell_output)
h_state = outputs[-1]

"""
    3、设置loss function和优化器，展开训练并完成测试
"""
#上面的LSTM部分的输出是一个[hidden_size]的tensor，需要分类的话，需要接入一个softmax层
#定义softmax层
out_w = tf.placeholder(tf.float32, [hidden_size, class_num], name='out_weights')
out_bias = tf.placeholder(tf.float32, [class_num], name='out_bias')
#开始训练额测试
W = tf.Variable(tf.truncated_normal([hidden_size, class_num], stddev=1.0), dtype=tf.float32)
bias = tf.Variable(tf.constant(0.1, shape=[class_num]), dtype=tf.float32)
y_pre = tf.nn.softmax(tf.matmul(h_state, W) + bias)

#损失函数和评估函数
cross_entropy = -tf.reduce_mean(y * tf.log(y_pre))
train_op = tf.train.AdamOptimizer(lr).minimize(cross_entropy)

correct_prediction = tf.equal(tf.argmax(y_pre, 1), tf.argmax(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

sess.run(tf.glorot_normal_initializer())
for i in range(2000):
    batch_size_ = 128
    batch = mnist.train.next_batch(batch_size_)
    if ( i + 1 ) % 200 == 0:
        train_accuracy = sess.run(accuracy, feed_dict={X:batch[0], y:batch[1], keep_prob:1.0, batch_size:batch_size_})
        #已经完成的步数
        print("Iter {0}, step {1}, training accuracy {2}".format(mnist.train.epochs_completed, (i+1), train_accuracy))
    sess.run(train_op, feed_dict={X:batch[0], y:batch[1], keep_prob:0.5, batch_size:batch_size_})
#计算测试数据准确率
print('test accuracy {0}'.format(sess.run(accuracy, feed_dict={X:mnist.test.images, y:mnist.test.labels, keep_prob:1.0, batch_size:mnist.test.images.shape[0]})))











































if __name__ == '__main__':
    #main()
    rnn_model(None, None)
