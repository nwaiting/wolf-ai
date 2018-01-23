#coding=utf8
"""
添加神经层
"""
import tensorflow as tf
import numpy as np

def add_layer(inputs, in_size, out_size, activation_function=None):
    Weights = tf.Variable(tf.random_normal([in_size, out_size]))
    biases = tf.Variable(tf.zeros([1, out_size]) + 0.1)
    Wx_plus_b = tf.matmul(inpus, Weights)
    outputs = None
    if activation_function is None:
        outputs = Wx_plus_b
    else:
        outputs = activation_function(Wx_plus_b)
    return outputs

def main():
    with tf.Session() as sess:
        print(sess.run(tf.random_normal([2,2])))

    x_data = np.linspace(1, 2, 10)[:, np.newaxis]
    print(x_data)
if __name__ == '__main__':
    main()
