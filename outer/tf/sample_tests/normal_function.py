#coding=utf-8

"""
http://blog.csdn.net/u014595019/article/details/52805444
http://blog.csdn.net/mydear_11000/article/details/53197891
"""

import tensorflow as tf

def main():
    #生成全是1的矩阵
    tensora = [[1,2,3],[4,5,6]]
    a = tf.ones([2,2],dtype=tf.float32)
    #生成shape大小一样的矩阵
    a1 = tf.ones_like(tensora, dtype=tf.float32)

    #生产全是0的矩阵
    b = tf.zeros([2,2], dtype=tf.float32)
    b1 = tf.zeros_like(tensora,dtype=tf.float32)

    #用设置的数值 生成填充的矩阵
    c = tf.fill([2,2], 2.)

    #常量
    d1 = tf.constant(2, shape=[2], dtype=tf.float32)
    d2 = tf.constant(2, shape=[2,2], dtype=tf.float32)
    d3 = tf.constant([1,2,3], shape=[6], dtype=tf.float32)
    d4 = tf.constant([1,2,3], shape=[3,2], dtype=tf.float32, name='const_shape6')

    #变量复用
    with tf.variable_scope('variable_scope1') as vari_scope:
        e1 = tf.get_variable(name='const_shape6', shape=[3,2])

    with tf.variable_scope('variable_scope1', reuse=True) as vari_scope:
        e2 = tf.get_variable('const_shape6')

    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        print(sess.run(a))
        print(sess.run(a1))
        print(sess.run(b))
        print(sess.run(b1))
        print(sess.run(c))
        print(sess.run(d1))
        print(sess.run(d2))
        print(sess.run(d3))
        print(sess.run(d4))
        print('get variable ', sess.run(e1))
        print('get variable ', sess.run(e2))
        print('end=============')

def matrix_function():
    #矩阵变换相关
    tensor_data = [[1,2,3],[4,5,6]]
    shape = tf.shape(tensor_data)

    #张量加1维  后面的0、1都是添加位置的索引
    tensor_expand1 = tf.shape(tf.expand_dims(tensor_data, 0))
    tensor_expand2 = tf.shape(tf.expand_dims(tensor_data, 1))
    tensor_expand3 = tf.expand_dims(tensor_data, -1)
    with tf.Session() as sess:
        print(sess.run(shape))
        print(sess.run(tensor_expand1))
        print(sess.run(tensor_expand2))
        print(sess.run(tensor_expand3))
        print('end ==========')

def combin_tensor():
    # 二维数组中 shape为(2,3)
    t1 = [[1,2,3],[4,5,6]]
    t2 = [[7,8,9],[10,11,12]]
    d1 = [[[1,1,1],[2,2,2]],[[3,3,3],[4,4,4]]]
    # 三维数组中 shape为(2,2,3)
    d2 = [[[5,5,5],[6,6,6]],[[7,7,7],[8,8,8]]]
    # 类似 tf.pack() 新版本的名字 tf.stack()
    #前面的0 1 2参数表示:
    # 在二维向量中， 0表示行 1表示列
    x1 = tf.concat([t1,t2], 0)
    x2 = tf.concat([t1,t2], 1)

    # 在三维向量中， 0表示纵向 1表示行 2表示列
    y1 = tf.concat([d1,d2], 0)
    y2 = tf.concat([d1,d2], 1)
    y3 = tf.concat([d1,d2], 2)
    with tf.Session() as sess:
        print(x1, sess.run(x1))
        print(x2, sess.run(x2))
        print('three ')
        print(y1, sess.run(y1))
        print(y2, sess.run(y2))
        print(y3, sess.run(y3))
        print('end===============')

def negative_function():
    a = [1,2,3,4]
    # 负采样
    nega_a = tf.negative(a)  #[-1,-2,-3,-4]
    with tf.Session() as sess:
        nega_a_res = sess.run(nega_a)
        print(tf.shape(nega_a_res), nega_a_res)

def func1():
    """
    tf.reduce_mean()中的reduction_indices参数表示函数的处理维度
    reduction_indices默认的参数是None，当传入0或者1或者[0,1]或者[1,0]时 转成的维度见如下：
    1 1 1
    1 1 1      ->(1)    3 3

      |(0)      \([0,1]或者[1,0])
                 \
    2 2 2               6
    """
    tensor_a = tf.Variable(tf.ones([2,3], dtype=tf.int32), dtype=tf.int32)
    res1 = tf.reduce_mean(tensor_a,reduction_indices=None)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        print(sess.run(tensor_a))
        print(sess.run(res1))

def func2():
    tensor_a = tf.constant('hello world')
    # 指定操作的设备，设备可以本地的CPU或者GPU，也可以是某一台远程的服务器
    with tf.device('/cpu:0'):
        # 设置在运行时输出运行的设备
        with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
            res = sess.run(tensor_a)
            print(type(res), res, res.decode())

if __name__ == '__main__':
    #main()
    #matrix_function()
    #combin_tensor()
    #negative_function()
    #func1()
    func2()
