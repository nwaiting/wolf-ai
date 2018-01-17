#coding=utf-8

"""
word2vec中有两个模型：
    1、CBOW模型
        已知上下文 预测当前词语
        对于小数据集有效
    2、Skip-gram模型
        已知当前词 预测上下文
        对于大数据集有效
    训练模型采用最大化似然概率作为目标函数，可以转化为极大化似然函数
    然而在使用word2vec方法进行特性学习的时候，并不需要计算全概率模型。在CBOW模型和skip-gram模型中，使用了逻辑回归（logistic regression）二分类方法进行的预测
    如CBOW模型，为了提高模型的训练速度和改善词向量的质量，通常采用随机负采样（Negative Sampling）的方法，噪音样本w1，w2，w3，wk…为选中的负采样
"""

import tensorflow as tf

def main():
    vocabulary_size = 0
    embedding_size = 0
    # 构建词向量变量
    embeddings = tf.Variable(tf.random_uniform([vocabulary_size, embedding_size], -1.0, 1.0), dtype=tf.float32)

    # 定义负采样中逻辑回归的权重和偏置
    nce_weiths = tf.Variable(tf.truncated_normal([vocabulary_size, embedding_size], stddev=1.0/tf.sqrt(embedding_size)))
    nce_biases = tf.Variable(tf.zeros([vocabulary_size]))

    #训练数据
    batch_size = 0
    train_inputs = tf.placeholder(tf.float32, shape=[batch_size])
    train_labels = tf.placeholder(tf.float32, shape=[batch_size, 1])

    #根据训练数据的寻找对应的词向量
    embed = tf.nn.embedding_lookup(embeddings, train_inputs)

    #基于负采样方法计算loss
    num_sampled = 0
    learn_rate = 0.01
    loss = tf.reduce_mean(tf.nn.nce_loss(weights=nce_weiths, biases=nce_biases, labels=train_labels, inputs=embed, num_classes=vocabulary_size, num_sampled=num_sampled))

    #随机梯度下降优化损失函数
    train_optimizer = tf.train.GradientDescentOptimizer(learn_rate).minimize(loss=loss)

    def generator_batch():
        yield 0

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for inputs,labels in generator_batch():
            _,curr_loss = sess.run([train_optimizer, loss], feed_dict={train_inputs:inputs, train_labels:labels})
            print('loss : {0}'.format(curr_loss))

def func2():
    # size为隐藏神经元的数量
    size = 0
    lstm_cell = tf.nn.rnn_cell.BasicLSTMCell(size, forget_bias=0.0, state_is_tuple=True)

    #训练中为了保证鲁棒性 定义dropout操作
    tf.nn.rnn_cell.DropoutWrapper(lstm_cell, output_keep_prob=config.keep_prob)

    #根据层数配置 定义多层RNN的神经网络
    tf.nn.rnn_cell.MultiRNNCell()

if __name__ == '__main__':
    main()
