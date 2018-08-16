#coding=utf-8

import tensorflow as tf

def func1():
    """
    tf.reset_default_graph()
        remove nodes from graph or reset entire default graph
        清除每次运行时，tensorflow中不断增加的节点并重置整个defualt graph
        默认图形是当前线程的一个属性。该tf.reset_default_graph函数只适用于当前线程。当一个tf.Session或者tf.InteractiveSession激活时调用这个函数会导致未定义的行为。调用此函数后使用任何以前创建的tf.Operation或tf.Tensor对象将导致未定义的行为
    """
    tf.reset_default_graph()
    with tf.variable_scope('space_a'):
        a = tf.constant([1,2,3])
    with tf.variable_scope('space_b'):
        b = tf.constant([4,5,6])
    with tf.Session() as sess:
        print(sess.run(a))
        print(sess.run(b))

def func2():
    """
    tf.nn.top_k(input, k, name=None)
        这个函数的作用是返回 input 中每行最大的 k 个数，并且返回它们所在位置的索引
    tf.nn.in_top_k(predictions, targets, k, name=None)
        targets 是predictions中的索引位，并不是 predictions 中具体的值
        targets对应的索引是否在最大的前k(2)个数据中
    """
    input = tf.constant(np.random.rand(3,4))
    k = 2
    output1 = tf.nn.top_k(input, k)
    output2 = tf.nn.in_top_k(input, [3,3,3], k)
    with tf.Session() as sess:
        print(sess.run(input))
        """
        [[ 0.98925872  0.15743092  0.76471106  0.5949957 ]
         [ 0.95766488  0.67846336  0.21058844  0.2644312 ]
         [ 0.65531991  0.61445187  0.65372938  0.88111084]]
        """
        print(sess.run(output1))
        """
        output1(values=array([[ 0.98925872,  0.76471106],
           [ 0.95766488,  0.67846336],
           [ 0.88111084,  0.65531991]]), indices=array([[0, 2],
           [0, 1],
           [3, 0]]))
        """
        print(sess.run(output2))
        """
            [False False  True]
        """

if __name__ == '__main__':
    #func1()

    func2()
