#coding=utf-8
import os
import time
import numpy as np
import tensorflow as tf
from tensorflow.contrib import rnn

class RNNChar(object):
    def __init__(self, num_classes,
                time_steps=28,
                time_inputs=28,
                hidden_size=128,
                num_layers=2,
                learning_rate=0.001,
                grad_clip=5,
                sampling=False,
                training_keep_prob=0.5,
                use_embedding=False,
                embedding_size=300,
                model_path = None,
                max_steps = 10000,
                save_every_step = 1000,
                log_every_step = 100
                ):
        self.num_classes_ = num_classes
        self.time_steps_ = time_steps
        self.time_inputs_ = time_inputs
        self.hidden_size_ = hidden_size
        self.num_layers_ = num_layers
        self.learning_rate_ = learning_rate
        self.grad_clip_ = grad_clip
        self.sampling_ = sampling
        self.training_keep_prob_ = training_keep_prob
        self.use_embedding_ = use_embedding
        self.embedding_size_ = embedding_size
        self.model_path_ = model_path
        self.max_steps_ = max_steps
        self.save_every_step_ = save_every_step
        self.log_every_step_ = log_every_step

        self.inputs_ = None
        self.targets_ = None
        self.keep_prob_ = None
        self.lstm_inputs_ = None
        self.initial_state_ = None
        self.lstm_outputs_ = None
        self.final_state_ = None
        self.logits_ = None
        self.session_ = None
        self.loss_ = None
        self.preprob_prediction_ = None

        tf.reset_default_graph()
        self.build_inputs()
        self.build_lstm()
        self.build_loss()
        self.build_optimizer()
        self.saver_ = tf.train.Saver()

    def build_inputs(self):
        with tf.name_scope('inputs'):
            self.inputs_ = tf.placeholder(tf.int32, shape=(self.time_steps_, self.time_inputs_), name='inputs')
            self.targets_ = tf.placeholder(tf.int32, shape=(self.time_steps_, self.time_inputs_), name='targets')
            self.keep_prob_ = tf.placeholder(tf.float32, name='keep_prob')

            if self.use_embedding_:
                with tf.device('/cpu:0'):
                    embeddings = tf.get_variable('embedding', [self.num_classes_, self.embedding_size_])
                    self.lstm_inputs_ = tf.nn.embedding_lookup(embeddings, self.inputs_)
            else:
                self.lstm_inputs_ = tf.one_hot(self.inputs_, self.num_classes_)

    def build_lstm(self):
        def get_lstm_cell(hidden_size, keep_prob):
            lstm_cell = rnn.BasicLSTMCell(hidden_size)
            droper = rnn.DropoutWrapper(lstm_cell, output_keep_prob=keep_prob)
            return droper

        with tf.name_scope('lstm'):
            #构造网络
            cells = rnn.MultiRNNCell([get_lstm_cell(self.hidden_size_, self.keep_prob_) for _ in range(self.num_layers_)], state_is_tuple=True)
            self.initial_state_ = cells.zero_state(self.time_steps_, tf.float32)

            #对网络状态cells进行网络展开
            self.lstm_outputs_, self.final_state_ = tf.nn.dynamic_rnn(cells, self.lstm_inputs_, initial_state=self.initial_state_)

            #通过outputs得到概率 !!!!!!!!
            steps_outputs = tf.concat(self.lstm_outputs_, 1)
            steps_outputs = tf.reshape(steps_outputs, (-1, self.hidden_size_))

            with tf.variable_scope('softmax'):
                softmax_w = tf.Variable(tf.truncated_normal([self.hidden_size_, self.num_classes_], stddev=0.1))
                softmax_b = tf.Variable(tf.zeros(self.num_classes_))

            #self.logits_ = tf.multiply(steps_outputs, softmax_w) + softmax_b
            self.logits_ = tf.matmul(steps_outputs, softmax_w) + softmax_b
            self.preprob_prediction_ = tf.nn.softmax(self.logits_, name='predictions')

    def build_loss(self):
        with tf.name_scope('loss'):
            real_targets = tf.one_hot(self.targets_, self.num_classes_)
            real_targets = tf.reshape(real_targets, self.logits_.get_shape())

            loss = tf.nn.softmax_cross_entropy_with_logits(logits=self.logits_, labels=real_targets)
            self.loss_ = tf.reduce_mean(loss)

    def build_optimizer(self):
        #返回所有的参数
        train_variables = tf.trainable_variables()

        #同时通过clipping gradients解决梯度爆炸的问题
        grads,_ = tf.clip_by_global_norm(tf.gradients(self.loss_, train_variables), self.grad_clip_)

        train_op = tf.train.AdamOptimizer(self.learning_rate_)

        #应用梯度修剪
        self.optimizer_ = train_op.apply_gradients(zip(grads, train_variables))

    def train(self, batchs):
        self.session_ = tf.Session()
        model_name = os.path.join(self.model_path_, 'model.{0}'.format(time.time()))
        sess = self.session_
        sess.run(tf.global_variables_initializer())
        #train network
        tmp_step = 0
        new_state = sess.run(self.initial_state_)
        begin_time = time.time()
        for X,y in batchs:
            tmp_step += 1
            feeds = {self.inputs_:X,
                    self.targets_:y,
                    self.keep_prob_:self.training_keep_prob_,
                    self.initial_state_:new_state}
            batch_loss,opt,new_state = sess.run([self.loss_, self.optimizer_, self.final_state_],feed_dict=feeds)

            if tmp_step % self.log_every_step_ == 0:
                print('step {0}/{1},'.format(tmp_step, self.max_steps_),
                    'loss {0},'.format(batch_loss),
                    'cost {0}'.format(time.time() - begin_time))
                begin_time = time.time()

            if tmp_step % self.save_every_step_ == 0:
                self.saver_.save(sess, model_name, global_step=tmp_step)

            if tmp_step >= self.max_steps_:
                break
        self.saver_.save(sess, model_name, global_step=tmp_step)

    def select_top_k(self, preds, vocab_size, top_k=5):
        p = np.squeeze(preds)
        p[np.argsort(p)[:-top_k]] = 0
        p = p / np.sum(p)
        c = np.random.choice(vocab_size, 1, p=p)
        return c

    def example(self, max_length, start, vocab_size):
        samples = [i for i in start]
        sess = self.session_
        new_state = sess.run(self.initial_state_)
        predictions = np.ones((vocab_size,)) # for start is []
        for c in start:
            x = np.zeros((1,1))
            # 输入单个字符
            x[0,0] = c
            feeds = {self.inputs_:x,
                    self.keep_prob_:self.training_keep_prob_,
                    self.initial_state_:new_state}
            pred,new_state = sess.run([self.preprob_prediction_, self.final_state_], feed_dict=feeds)
        c = self.select_top_k(pred, vocab_size)
        samples.append(c)

        #生成新的字符
        for i in range(max_length):
            x = np.ones((1,1))
            x[0,0] = c
            feeds = {self.inputs_:x,
                    self.keep_prob_:self.training_keep_prob_,
                    self.initial_state_:new_state}
            pred,new_state = sess.run([self.preprob_prediction_, self.final_state_], feed_dict=feeds)
            c = self.select_top_k(pred, vocab_size)
            samples.append(c)
        return np.array(samples)

    def load(self, checkpoint):
        self.session_ = tf.Session()
        self.saver_.restore(self.session_, checkpoint)
        print('Restored from {0}'.format(checkpoint))
