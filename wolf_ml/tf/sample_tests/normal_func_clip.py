#coding=utf-8

import tensorflow as tf


def func1():
    """
    tf.clip_by_value(
            t,
            clip_value_min,
            clip_value_max,
            name=None
        )
    截断，常和对数函数一起使用，如：
        crose_ent = -tf.reduce_mean(tf.log(y_*tf.clip_by_value(y, 1e-10, 1.)))  计算交叉熵
    t：待处理的tensor，或是一个list等
    clip_value_min：需要过滤的最小值，若t中存在比该值还小的值，一律换成clip_value_min
    clip_value_max：需要过滤的最大值，若t中存在比该值还大的值，一律换成clip_value_max
    """
    pass

def func2():
    """
    clip_by_global_norm(t_list, clip_norm, use_norm=None, name=None)
        修正梯度值，用于控制梯度爆炸的问题。梯度爆炸是由于链式法则求导的关系，导致梯度的指数级衰减。如果梯度不加限制，则可能因为迭代中梯度过大导致训练难以收敛
        Grandient Clipping 作用就是控制权重的更新在一个合理的范围
        通过权重梯度的综合的比率来截取多个张量的值
        params:
            t_list：待修剪的张量
            clip_norm：表示修剪的比例(clipping ratio)
        return:
            list_clipped：修剪后的张量
            global_norm：一个中间计算量，一个所有张量的全局范数
    """















if __name__ == '__main__':
    #func1()

    func2()
