#coding=utf-8

import tensorflow as tf

def func1():
    from tensorflow.contrib.crf import crf_log_likelihood
    """
    crf_log_likelihood(inputs,tag_indices,sequence_lengths,transition_params=None)：
        使用crf来计算损失，用到的优化方法为：最大似然估计
        如果你预测的是个序列，那么可以选择crf_log_likelihood作为损失函数
        params：
            inputs: 一个形状为[batch_size, max_seq_len, num_tags] 的tensor,一般使用BILSTM处理之后输出转换为他要求的形状作为CRF层的输入
                    就是每个标签的预测概率值，这个值根据实际情况选择计算方法
            tag_indices: 一个形状为[batch_size, max_seq_len] 的矩阵,其实就是真实标签 !!!!!
            sequence_lengths: 一个形状为 [batch_size] 的向量,表示每个序列的长度
                            这是一个样本真实的序列长度，因为为了对齐长度会做些padding，但是可以把真实的长度放到这个参数里
            transition_params: 形状为[num_tags, num_tags] 的转移矩阵
                        转移概率，这个可以没有，没有的话这个函数也会计算出来
        return：
            log_likelihood: 标量,log-likelihood
            transition_params: 形状为[num_tags, num_tags] 的转移矩阵
    """
    pass

def func2():
    from tensorflow.contrib.crf import viterbi_decode
    """
    viterbi_decode(score,transition_params)
        作用就是返回最好的标签序列，这个函数只能在测试时使用，在TensorFlow外部解码
        params:
            score: 一个形状为[seq_len, num_tags] matrix of unary potentials.
            transition_params: 形状为[num_tags, num_tags] 的转移矩阵
        return:
            viterbi: 一个形状为[seq_len] 显示了最高分的标签索引的列表.
            viterbi_score: A float containing the score for the Viterbi sequence.
    """
    pass


def func3():
    from tensorflow.contrib.crf import crf_decode
    """
    crf_decode(potentials,transition_params,sequence_length)
        在TensorFlow内部解码
        params:
            potentials：一个形状为[batch_size, max_seq_len, num_tags] 的tensor
            transition_params: 一个形状为[num_tags, num_tags] 的转移矩阵
            sequence_length: 一个形状为[batch_size] 的 ,表示batch中每个序列的长度
        return:
            decode_tags:一个形状为[batch_size, max_seq_len] 的tensor,类型是tf.int32.表示最好的序列标记
            best_score: 有个形状为[batch_size] 的tensor, 包含每个序列解码标签的分数
    """
    pass

if __name__ == '__main__':
    main()
