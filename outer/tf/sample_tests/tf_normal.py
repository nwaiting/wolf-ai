#coding=utf8

import tensorflow as tf

def main():
    #从正态分布输出随机数 一维的数组
    a = tf.Variable(tf.random_normal([10], dtype=tf.float32, seed=1))
    #截断的正态分布函数 一维的数组
    b = tf.Variable(tf.truncated_normal([10], dtype=tf.float32, seed=2))
    #从均匀分布中返回随机值 一维的数组
    c = tf.Variable(tf.random_uniform([10], -1.0, 1.0, seed=3))
    #沿着要被洗牌的张量的第一个维度随机打乱
    d_before = tf.Variable(tf.truncated_normal([3,3], seed=4))
    d = tf.Variable(tf.random_shuffle(d_before))
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        print('begin')
        print(sess.run(a))
        print(sess.run(b))
        print(sess.run(c))
        print('============= before ', sess.run(d_before))
        print('============= after ', sess.run(d))
        print('end')

def my_add(a, b):
    xa = tf.placeholder(dtype=tf.float32)
    xb = tf.placeholder(dtype=tf.float32)
    y = tf.add(xa, xb)
    with tf.Session() as sess:
        y_result = sess.run(y, feed_dict={xa:a,xb:b})
        print(tf.shape(y_result),y_result)

def functions_1():
    #variable_a = tf.Variable(tf.random_normal([10], dtype=tf.float32, seed=1))
    variable_a = tf.Variable(tf.random_uniform([10], 0., 10., seed=1, dtype=tf.float32))
    #只能输出int类型 输出最大值最小值索引
    variable_b = tf.argmax(input=variable_a)
    variable_c = tf.argmax(input=variable_a)
    variable_d = tf.argmin(input=variable_a)
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        print(tf.shape(variable_a), sess.run(variable_a))
        print(tf.shape(variable_b), sess.run(variable_b))
        print(tf.shape(variable_c), sess.run(variable_c))
        print(tf.shape(variable_d), sess.run(variable_d))

def function_2():
    a = [1,2,3]
    b = [4,2,6]
    result = tf.equal(a, b)
    #返回的结果 [False  True False]
    with tf.Session() as sess:
        print(tf.shape(result), sess.run(result))

def function_3():
    # 数据类型转换 tf.cast()
    var_a = tf.Variable([1,0,3])
    #结果 [ True False  True]
    var_b = tf.cast(var_a, dtype=tf.bool)
    #结果  [ 1.  0.  3.]
    var_c = tf.cast(var_a, dtype=tf.float32)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        print(tf.shape(var_a), sess.run(var_a))
        print(tf.shape(var_b), sess.run(var_b))
        print(tf.shape(var_c), sess.run(var_c))

def function_4():
    #矩阵乘法
    var_a = tf.Variable(tf.random_uniform([2,2], 1, 5, dtype=tf.float32), dtype=tf.float32)
    var_b = tf.Variable(tf.truncated_normal([2,2], dtype=tf.float32))

    y = tf.matmul(var_a, var_b)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        print(sess.run(var_a))
        print(sess.run(var_b))
        print(tf.shape(y), sess.run(y))

def function_5():
    """
    tf.reshape()
    """
    var_a = tf.Variable(tf.random_uniform([3,4], 1., 5., dtype=tf.float32))
    var_b = tf.reshape(var_a, [2,6])
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        print(var_a, sess.run(var_a))
        print(var_b, sess.run(var_b))

def function_6():
    """
    tf.nn.embedding_lookup(embedding, input_ids)
    根据input_ids中的索引，寻找embedding中对应的元素
    比如：input_ids=[1,3,5]，则找到embedding中下标为1,3,5的向量组成一个矩阵返回
    """
    tensor = tf.Variable(tf.random_normal([5,5], dtype=tf.float32))
    tensor_int = tf.cast(tensor, dtype=tf.int32)
    input_ids = tf.placeholder(dtype=tf.int32, shape=[None, None])
    embedding = tf.Variable(tensor_int)
    input_embedding = tf.nn.embedding_lookup(embedding, input_ids)

    input_ids_2 = tf.Variable([1,2,3])
    input2_embedding = tf.nn.embedding_lookup(embedding, input_ids_2)
    input_ids_3 = tf.Variable([[0,1], [1,2]])
    input3_embedding = tf.nn.embedding_lookup(embedding, input_ids_3)
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        print(sess.run(embedding))
        #print(sess.run(input_embedding, feed_dict={input_ids:[1,2,3]}))
        print('========= input_embedding')
        print(sess.run(input_embedding, feed_dict={input_ids:[[0,1], [0,1]]}))
        print('========= input2_embedding')
        print(sess.run(input2_embedding))
        print('========== input3_embedding')
        print(sess.run(input3_embedding))

def function_7():
    """
    tf.gradients(ys, xs)
    计算梯度的函数tf.gradients(ys, xs)，注意xs中的x必须与ys相关，不相关的话会报错

    matmul()矩阵相乘;
    multiply()实数相乘
    """
    w1 = tf.Variable([[1,2]])
    w2 = tf.Variable([[3,4]])
    res = tf.matmul(w1, [[2], [1]])
    grads = tf.gradients(res, [w1])

    a = tf.constant(2., dtype=tf.float32)
    b = tf.constant(3, dtype=tf.float32)
    c = tf.pow(a, b) # 表示 a^b
    grad = tf.gradients(ys=c, xs=a) #一阶对a导数
    grad_2 = tf.gradients(ys=grad[0], xs=a) #二阶对a求导
    grad_3 = tf.gradients(ys=grad_2[0], xs=a) #三阶对a求导

    grad_b = tf.gradients(ys=c, xs=b) #一阶对b求导

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        print(sess.run(grads))
        print(sess.run(c))
        print(sess.run(grad))
        print(sess.run(grad_2))
        print(sess.run(grad_3))
        print(sess.run(grad_b)) # (a^b)' = (a^b)lna

def function_8():
    """
    tf.linspace()
    tf.range()
    """
    line_tensor = tf.linspace(1., 5., 10) #等差数列
    range_tensor = tf.range(1, 10) #rang序列
    with tf.Session() as sess:
        print(sess.run(line_tensor))
        print(sess.run(range_tensor))

def function_9():
    """
    tf.assign(a, b) 用b赋值给a
    """
    h_a = tf.Variable(1., dtype=tf.float32)
    h_b = tf.Variable(2., dtype=tf.float32)
    h_c = tf.Variable(0., dtype=tf.float32)
    h_add = tf.add(h_a, h_b)
    h_update = tf.assign(h_c, h_add)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        print(sess.run(h_c))
        print(sess.run(h_update))
        print(sess.run(h_c))

def function_10():
    """
    另类执行run的写法
    """
    tensor_a = tf.constant('hello world')
    tensor_b = tf.Variable(tf.random_uniform([10], 0., 5., dtype=tf.float32))
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        print(tensor_a.eval())
        print(type(tensor_b.eval()))
        tensor_a_val = tensor_a.eval(session=sess)
        print(tensor_a_val)

def function_reduce():
    """
    求平均值 可以指定求第一维、指定维数的平均值
    tf.reduce_mean()
    求最大值 可以指定位维度
    tf.reduce_max()
    求和 可以指定维度
    tf.reduce_sum()
    """

def function_bak():
    # 将一个数字序列ids转化为embedding序列
    tf.nn.embedding_lookup()

    #返回所有可训练的变量
    tf.trainable_variables()

    #计算导数
    tf.gradients()

    #修正梯度值 用于控制梯度爆炸或者梯度弥散，原因都是链式法则求导的原因
    tf.clip_by_global_norm()

    #按照概率随机丢掉一些
    tf.nn.dropout()

    #产生等差序列
    # tf.linspace在[start,stop]范围内产生num个数的等差数列。不过注意，start和stop要用浮点数表示，不然会报错
    tf.linspace()
    #tf.range在[start,limit)范围内以步进值delta产生等差数列。注意是不包括limit在内的
    tf.range()

    # 更新模型中的参数
    tf.assign()

    #规范化
    #变量添加命名域
    tf.variable_scope()
    #返回当前变量的命名域
    tf.get_variable_scope()

if __name__ == '__main__':
    #main()
    #my_add(1,2)
    #functions_1()
    #function_2()
    #function_3()
    #function_4()
    #function_5()
    #function_6()
    #function_7()
    #function_8()
    #function_9()
    function_10()
