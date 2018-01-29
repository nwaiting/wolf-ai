#coding=utf-8
from __future__ import print_function
import tensorflow as tf
from tensorflow.contrib.tensor_forest.python import tensor_forest
from tensorflow.python.ops import resources
from tensorflow.examples.tutorials.mnist import input_data
import matplotlib.pyplot as plt

import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''

def main():
    current_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
    mnist = input_data.read_data_sets(current_path, one_hot=False)
    # Parameters
    num_steps = 500 # Total steps to train
    batch_size = 1024 # The number of samples per batch
    num_classes = 10 # The 10 digits
    num_features = 784 # Each image is 28x28 pixels
    num_trees = 10
    max_nodes = 1000
    X = tf.placeholder(tf.float32, shape=[None, num_features])
    # For random forest, labels must be integers (the class id)
    Y = tf.placeholder(tf.int32, shape=[None])

    # Random Forest Parameters
    hparams = tensor_forest.ForestHParams(num_classes=num_classes,
                                        num_features=num_features,
                                        num_trees=num_trees,
                                        max_nodes=max_nodes
                                        ).fill()
    # build Random Forest
    forest_graph = tensor_forest.RandomForestGraphs(hparams)
    # get train
    forest_graph_train = forest_graph.training_graph(X, Y)
    # get loss
    forest_graph_loss = forest_graph.training_loss(X, Y)

    #measure the accuracy
    infer_op_, _, _ = forest_graph.inference_graph(X)
    correct_prediction = tf.equal(tf.argmax(infer_op_, 1), tf.cast(Y, tf.int64))
    accuracy_op = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    init_vars = tf.group(tf.global_variables_initializer(), resources.initialize_resources(resources.shared_resources()))

    with tf.Session() as sess:
        sess.run(init_vars)
        for i in range(num_steps):
            batch_x, batch_y = mnist.train.next_batch(batch_size)
            _, l = sess.run([forest_graph_train, forest_graph_loss], feed_dict={X:batch_x, Y:batch_y})
            if 50 % i == 0:
                acc = sess.run(accuracy_op, feed_dict={X:batch_x, Y:batch_y})
                print('step {0} loss {1} accuracy {2}'.format(i, l, acc))

    # test model
        test_x, test_y = mnist.test.images, mnist.test.labels
        print('test accuracy {0}'.format(sess.run(accuracy_op, feed_dict={X:test_x, Y:test_y})))






















if __name__ == '__main__':
    main()
