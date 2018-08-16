#coding=utf-8

import tensorflow as tf

def func1():
    """
    tf.shape()：
        获取变量的shape
    """
    t = tf.Variable(tf.random_normal([10, 100]))
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        print(tf.shape(t))
        print(sess.run(tf.shape(t)))

def func2():
    """
    tf.nn.softmax()：

    tf.argmax(input, dimension, name=None)
        dimension：dimension=0 按列找,dimension=1 按行找
    """
    y = tf.nn.softmax([1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0]) # tf.argmax(y, 0) 结果为10
    y = tf.nn.softmax([[1.5],[2.5],[3.5],[4.5],[3.5],[4.5],[7.5],[4.5],[9.5],[10.5]])
    y = tf.nn.softmax([[1.5,2.5],[3.5,4.5]])  # tf.argmax(y, 1) 结果为[1 1]
    with tf.Session() as sess:
        print(sess.run(y))
        print(sess.run(tf.argmax(y, 1)))

def func3():
    """
    初始化：
        tf.global_variables_initializer()
            添加节点用于初始化所有的变量(GraphKeys.VARIABLES)。返回一个初始化所有全局变量的操作，当构建完整个模型并在会话中加载模型后，运行这个节点
            能够将所有的变量一步到位的初始化，非常的方便
        tf.local_variables_initializer()
            初始化所有局部变量的操作(GraphKeys.LOCAL_VARIABLE)。GraphKeys.LOCAL_VARIABLE中的变量指的是被添加入图中，但是未被存储的变量。tf.train.Saver中关于存储的变量

        tf.group(*inputs,**kwargs)
                input：需要进行分组的零个或多个张量。
                kwargs：构造 NodeDef 时要传递的可选参数
            流程控制函数
            创建一个操作，该操作可以对TensorFlow的多个操作进行分组。
            当这个操作完成后，所有input中的ops都已完成，这个操作没有输出
    """
    init_var = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
    with tf.Session() as sess:
        sess.run(init_var)

    #tf.group()
    w = tf.Variable(1)
    mul = tf.multiply(w,2)
    add = tf.add(w,2)
    group = tf.group(mul, add)
    tuple = tf.tuple([mul, add])
    with tf.Session() as sess:
        sess.run(group)
        sess.run(tuple)
        #上面两个run都会求tensor(add)和tensor(mul)的值，区别是：
        #tf.group()返回的是'op'，tf.tuple返回的是list of tensor。这样导致的结果是
        #sess.run(tuple)返回的是tensor(mul)和tensor(add)的值
        #sess.run(group)不会返回值

def func4():
    """
    模型的保存与恢复：
        保存：
            saver = tf.train.Saver(max_to_keep=0)
            saver.save(sess, 'mnist.ckpt', global_step=step)
            参数max_to_keep：设置保存模型的个数，
                            默认为5，保存最近的5个模型，
                            None或者0：表示每训练一轮(epoch)就想保存一次模型
                            1：只保存最新的一次的模型
            save函数参数：
                sess：回话
                第二个参数：保存的路径和名字
                第三个参数：训练的次数作为后缀加入到模型名字中
        恢复：
            saver = tf.train.Saver(tf.global_variables())
            saver.restore(sess, checkpoint)
            模型的恢复用的是restore()函数，它需要两个参数restore(sess, save_path)，save_path指的是保存的模型路径。
            我们可以使用tf.train.latest_checkpoint() 来自动获取最后一次保存的模型
    """
    pass

#通过启动传递参数
#python normal_function2.py --name namename
FLAGS = tf.flags.FLAGS
tf.flags.DEFINE_string('name', '10086', 'describe for name')

def main(_):
    print('this is test tf')
    print(FLAGS.name)

def func5():
    """
    在word2vec中会用到
    选取一个张量里面索引对应的元素：
        tf.nn.embedding_lookup(embedding, indexs)
    """
    embedding = [[1, 0, 0, 0, 0]
                 [0, 1, 0, 0, 0]
                 [0, 0, 1, 0, 0]
                 [0, 0, 0, 1, 0]
                 [0, 0, 0, 0, 1]]
    res = tf.nn.embedding_lookup(embedding, [1,2,3,0])
    res = [[0, 1, 0, 0, 0]
            [0, 0, 1, 0, 0]
            [0, 0, 0, 1, 0]
            [1, 0, 0, 0, 0]]
    #选取embedding中第一个，第二个，第三个，第0个元素


    res = tf.nn.embedding_lookup(embedding, [[1,2],[2,1],[3,3]])
    res = [[[0, 1, 0, 0, 0],[0, 0, 1, 0, 0]],
            [[0, 0, 1, 0, 0],[0, 1, 0, 0, 0]],
            [[0, 0, 0, 1, 0],[0, 0, 0, 1, 0]]]
    #选取embedding中的第一个，第二个组成新的矩阵的第一行
    #选择embedding中的第二个，第一个组成新的矩阵的第二行
    #选择embedding中的第三个，第三个组成新的矩阵的第三行

def func6():
    """
    tf.one_hot(
        indices,#输入，这里是一维的
        depth,# one hot dimension.
        on_value=None,#output 默认1
        off_value=None,#output 默认0
        axis=None,#根据我的实验，默认为1
        dtype=None,
        name=None
        )
    """
    label1=tf.constant([0,1,2,3,4,5,6,7])
    b = tf.one_hot(label1, 8)
    with tf.Session() as sess:
        print(sess.run(b))
    """
    b = [[1. 0. 0. 0. 0. 0. 0. 0.]
         [0. 1. 0. 0. 0. 0. 0. 0.]
         [0. 0. 1. 0. 0. 0. 0. 0.]
         [0. 0. 0. 1. 0. 0. 0. 0.]
         [0. 0. 0. 0. 1. 0. 0. 0.]
         [0. 0. 0. 0. 0. 1. 0. 0.]
         [0. 0. 0. 0. 0. 0. 1. 0.]
         [0. 0. 0. 0. 0. 0. 0. 1.]]
    """

    label1=tf.constant([[0,1,2],[3,4,5],[6,7,7]])
    b = tf.one_hot(label1, 8, dtype=tf.int32)
    with tf.Session() as sess:
        print(sess.run(b))
    """
    [[[1 0 0 0 0 0 0 0]
      [0 1 0 0 0 0 0 0]
      [0 0 1 0 0 0 0 0]]

     [[0 0 0 1 0 0 0 0]
      [0 0 0 0 1 0 0 0]
      [0 0 0 0 0 1 0 0]]

     [[0 0 0 0 0 0 1 0]
      [0 0 0 0 0 0 0 1]
      [0 0 0 0 0 0 0 1]]]
    """

def func7():
    """
    tf.variable_scope()
        主要用于管理一个graph中变量的名字，避免变量之间的命名冲突
        可以让变量有相同的命名，包括tf.get_variable()得到的变量，还有tf.Variable()的变量
    tf.name_scope()
        主要用于管理一个图里的各种op，避免各个op之间命名冲突
        可以让变量有相同的命名，但是只限于tf.Variable()的变量
    """

    #tf.variable_scope
    with tf.variable_scope('V1'):
        a1 = tf.get_variable(name='a1', shape=[1], initializer=tf.constant_initializer(1))
        a2 = tf.Variable(tf.random_normal(shape=[2,3], mean=0, stddev=1), name='a2')
    with tf.variable_scope('V2'):
        a3 = tf.get_variable(name='a1', shape=[1], initializer=tf.constant_initializer(1))
        a4 = tf.Variable(tf.random_normal(shape=[2,3], mean=0, stddev=1.0), name='a2')
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        print(a1.name)
        print(a2.name)
        print(a3.name)
        print(a4.name)

    #tf.name_scope
    with tf.name_scope('V1'):
        #错误
        #a1 = tf.get_variable(name='a1', shape=[1], initializer=tf.constant_initializer(1))
        a2 = tf.Variable(tf.random_normal(shape=[2,3], mean=0, stddev=1), name='a2')
    with tf.name_scope('V2'):
        #错误 a1和a3命名冲突，报错
        #a3 = tf.get_variable(name='a1', shape=[1], initializer=tf.constant_initializer(1))
        a4 = tf.Variable(tf.random_normal(shape=[2,3], mean=0, stddev=1), name='a2')
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        #print(a1.name)
        print(a2.name)
        #print(a3.name)
        print(a4.name)


if __name__ == '__main__':
    #func1()

    #func2()

    #func3()

    #func4()

    # 启动 main(_) 函数，注意main里面有一个参数
    #tf.app.run()

    #func5()

    func6()

    #func7()
