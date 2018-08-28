#coding=utf-8

import tensorflow as tf

def func1():
    """
    tf.nn.sparse_softmax_cross_entropy_with_logits(logits=net, labels=y)
        参数中的labels接受直接的数字标签，如[1],[2],[3],[4]（类型只能为int32, int64）
    tf.nn.softmax_cross_entropy_with_logits(logits=net, labels=y2)
        参数中的labels接受ont-hot标签，如[1,0,0,0], [0,1,0,0],[0,0,1,0], [0,0,0,1]（类型为int32，int64）
    """
    pass

def func2():
    """
    tf.nn.softmax_cross_entropy_with_logits(
    _sentinel=None,
    labels=None,
    logits=None,
    dim=-1,
    name=None
    )

    tf.nn.softmax_cross_entropy_with_logits_v2(
    _sentinel=None,
    labels=None,
    logits=None,
    dim=-1,
    name=None
    )
    """
    pass

if __name__ == '__main__':
    #func1()

    #func2()
