#coding=utf-8

"""
    pos tagger for building a lstm based pos tagging model
"""

from __future__ import print_function
import time
import numpy as np
import tensorflow as tf
from tensorflow.contrib import rnn
from tensorflow.contrib.legacy_seq2seq import sequence_loss_by_example
import sys
import os

pkg_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pkg_path)

lang = 'zh' if len(sys.argv) == 1 else sys.argv[1]
file_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(file_path, 'data', lang)
train_dir = os.path.join(file_path, 'ckpt', lang)

flags = tf.flags
logging = tf.logging
'''
    通过设置flags来传递tf.app.run()所需要的参数，可以直接在程序运行之前初始化flags，也可以在运行程序的时候设置命令行参数来传递参数
    第一个是参数名称，第二个是默认值，第三个是描述
    设置：
        flags.DEFINE_string('pos_data_path', data_path, 'data_path')
        FLAGS = tf.flags.FLAGS
    使用：
        print(FLAGS.pos_data_path)
'''
flags.DEFINE_string('pos_lang', lang, 'pos language option for model config')
flags.DEFINE_string('pos_data_path', data_path, 'data_path')
flags.DEFINE_string('pos_train_dir', train_dir, 'Training directory')
flags.DEFINE_string('pos_scope_name', 'pos_var_scope', 'Variable scope of pos Model')

FLAGS = tf.flags.FLAGS

class LargeConfigChinese(object):
    '''
        large config
    '''
    init_scale_ = 0.04
    learning_rate_ = 0.01
    max_grad_norm_ = 10
    num_layers_ = 2
    num_steps_ = 30
    hidden_size_ = 128
    max_epoch_ = 5
    max_max_epoch_ = 55
    keep_prob_ = 1.0
    lr_decay_ = 1/1.15
    batch_size_ = 1 #single sample batch
    bocab_size_ = 50000
    target_num_ = 44

class POSTagger(object):
    '''
        ths pos tagger model
    '''
    def __init__(self, is_training, config=None):
        if not config:
            config = LargeConfigChinese()
        self.batch_size_ = batch_size = config.batch_size
        self.num_steps_ = num_steps = config.num_steps_
        self.hidden_size_ = config.hidden_size_
        self.vocab_size_ = config.vocab_size_
        self.target_num_ = config.target_num_

        self.input_data_ = tf.placeholder(tf.int32, [batch_size, num_steps])
        self.targets_ = tf.placeholder(tf.int32, [batch_size, num_steps])

        # check if model is training
        self.is_training_ = is_training

        lstm_cell = rnn.BasicLSTMCell(self.hidden_size_, forget_bias=1.0, state_is_tuple=True)
        if self.is_training_ and config.keep_prob_ < 1:
            lstm_cell = rnn.DropoutWrapper(lstm_cell, output_keep_prob=config.keep_prob_)
        cell = rnn.MultiRNNCell([lstm_cell] * config.num_layers_, state_is_tuple=True)
        self.initial_state_ = cell.zero_state(batch_size, tf.float32)

        with tf.device('/cpu:0'):
            embedding = tf.get_variable('embedding', [self.vocab_size_, self.hidden_size_], dtype=tf.float32)
            inputs = tf.nn.embedding_lookup(embedding, self.input_data_)

        if self.is_training_ and config.keep_prob_ < 1:
            inputs = tf.nn.dropout(inputs, config.keep_prob_)

        outputs = []
        state = self.initial_state_
        with tf.variable_scope('pos_lstm'):
            for time_step in range(num_steps):
                if time_step > 0:
                    tf.get_variable_scope().reuse_variables()
                (cell_output, state) = cell(inputs[:, time_step, :], state)
                outputs.append(cell_output)

        output = tf.reshape(tf.concat(outputs, 1),[-1, self.hidden_size_])
        softmax_w = tf.get_variable('softmax_w', [self.hidden_size_, self.target_num_], dtype=tf.float32)
        softmax_b = tf.get_variable('softmax_b', [self.target_num_], dtype=tf.float32)
        logits = tf.matmul(output, softmax_w) + softmax_b
        loss = sequence_loss_by_example(logits=logits,
                                        targets=[tf.reshape(self.targets_, [-1])],
                                        weights=[tf.ones([self.batch_size_ * self.num_steps_], dtype=tf.float32)])

        # fetch result in session
        self.cost_ = cost = tf.reduce_mean(loss) / self.batch_size_
        self.final_state_ = state
        self.logits_ = logits

        # set optimizer and learning rate
        self.lr_ = tf.Variable(0.0, trainable=True)
        tvars = tf.trainable_variables()
        grads,_ = tf.clip_by_global_norm(tf.gradients(cost, tvars), config.max_grad_norm_)
        optimizer = tf.train.GradientDescentOptimizer(self.lr_)
        self.train_op_ = optimizer.apply_gradients(zip(grads, tvars))

        self.new_lr_ = tf.placeholder(tf.float32, shape=[], name='new_learning_rate')
        self.lr_update_ = tf.assign(self.lr_, self.new_lr_)
        self.saver_ = tf.train.Saver(tf.global_variables())

    def assign_lr(self, session, lr_value):
        session.run(self.lr_update_, feed_dict={self.new_lr_:lr_value})

    @property
    def lr(self):
        return self.lr_

def lstm_model(inputs, targets, config):
    config = LargeConfigChinese()
    batch_size = config.batch_size_
    num_steps = config.num_steps_
    num_layers = config.num_layers_
    hidden_size = config.hidden_size_
    vocab_size = config.vocab_size_
    target_num = config.target_num_

    lstm_model = rnn.BasicLSTMCell(hidden_size, forget_bias=0.0, state_is_tuple=True)
    cell = rnn.MultiRNNCell([lstm_model] * num_layers, state_is_tuple=True)

    initial_state = cell.zero_state(batch_size=batch_size, dtype=tf.float32)
    # outputs shape：list of tensor with shape [batch_size, hidden_size], length：time_step
    outputs = []
    state = initial_state
    with tf.variable_scope('pos_lstm'):
        for time_step in range(num_steps):
            if time_step > 0:
                tf.get_variable_scope().reuse_variables()
            # inputs[batch_size, time_step, hidden_size]
            (cell_output, state) = cell(inputs[;, time_step, :], state)
            outputs.append(cell_output)

    output = tf.reshape(tf.concat(outputs, 1), [-1, hidden_size])
    softmax_w = tf.get_variable('softmax_w', [hidden_size, target_num], dtype=tf.float32)
    softmax_b = tf.get_variable('softmax_b', [target_num], dtype=tf.float32)

    logits = tf.matmul(softmax_w, output) + softmax_b

    loss = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=tf.reshape())
    cost =


def bilstm_model(inputs, targets, config):
    pass



def run_epoch(session,model,word_data,tag_data,eval_op,verbose=False):
    '''
        runs the model on the given data
    '''
    epoch_size = ((len(word_data)//model.batch_size_) - 1) // model.num_steps_














def main():
    pass


if __name__ == '__main__':
    main()
