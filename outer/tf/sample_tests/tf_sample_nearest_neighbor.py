#coding=utf-8

import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data

# 参考 https://github.com/aymericdamien/TensorFlow-Examples/blob/master/examples/2_BasicModels/nearest_neighbor.py#L24

def main():
    mnist = input_data.read_data_sets('./outer/tf/sample_tests/data', one_hot=True)
    # 5000 for training(nn candidates)
    X_train,Y_train = mnist.train.next_batch(5000)
    X_test,Y_test = mnist.test.next_batch(200)

    x_tr = tf.placeholder(tf.float32, shape=[None, 784])
    x_te = tf.placeholder(tf.float32, shape=[784])

    #cal L1 distance
    distance = tf.reduce_sum(tf.abs(tf.add(x_tr, tf.negative(x_te))), reduction_indices=1)

    pred = tf.arg_min(distance, 0)

    accuracy = 0

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        for i in range(len(X_test)):
            nn_index = sess.run(pred, feed_dict={x_tr:X_train, x_te:X_test[i, :]})
            print('test : {0} Prediction : {1} True Class : {2}'.format(i, np.argmax(Y_train[nn_index]), np.argmax(Y_test[i])))
            if np.argmax(Y_train[nn_index]) == np.argmax(Y_test[i]):
                accuracy += 1./len(X_test)
        print('accuracy : {0}'.format(accuracy))

if __name__ == '__main__':
    main()
