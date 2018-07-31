#coding=utf-8

import tensorflow as tf
from tensorflow.contrib import rnn

rnn.BasicLSTMCell(lstm_size, forget_bias=1.0, state_is_tuple=True)
rnn.LSTMCell
'''
    rnn.BasicLSTMCell 是最简单的一个LSTM类，没有实现clipping、peep-hole等LSTM的高级变种，仅作为一个基本的basicline结构存在，
    如果需要使用高级变种，需要rnn.LSTMCell
    参数：
        lstm_size：一个cell中神经元的个数，
        forget_bias：The bias added to forget gates
'''


rnn.MultiRNNCell([lstm]*num_layers, state_is_tuple=True)
'''
    如果希望整个网络的层数更多（比如bi-lstm，两层的lstm cell），应该堆叠多个LSTM Cell，
'''


rnn.DropoutWrapper(lstm, output_keep_prob=1.0)
'''
    RNN和cnn的dropout不同，在不同的rnn中，时间序列方向不进行dropout，就是说从t-1时刻的状态传递到t时刻计算时，中间不进行memory的dropout，
    dropout仅用于上一层的输出做dropout
'''



























if __name__ == '__main__':
    main()
