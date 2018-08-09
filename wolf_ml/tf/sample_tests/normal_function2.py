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
    """


def func4():
    """
    模型的保存于恢复：
        恢复：
        saver = tf.train.Saver(tf.global_variables())
        saver.restore(sess, checkpoint)
        模型的恢复用的是restore()函数，它需要两个参数restore(sess, save_path)，save_path指的是保存的模型路径。
        我们可以使用tf.train.latest_checkpoint() 来自动获取最后一次保存的模型
    """
    pass


def main(_):
    print('this is test tf')

if __name__ == '__main__':
    #func1()

    #func2()

    #func3()

    #func4()

    # 启动 main(_) 函数，注意main里面有一个参数
    import tensorflow as tf
    tf.app.run()
