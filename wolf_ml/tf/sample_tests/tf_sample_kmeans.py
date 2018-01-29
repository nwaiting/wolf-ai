#coding=utf-8
from __future__ import print_function
import numpy as np
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.contrib.factorization import KMeans, KMeansClustering
#from tensorflow.contrib.bayesflow
#from tensorflow.contrib.boosted_trees
#from tensorflow.contrib.decision_trees
#from tensorflow.contrib.ffmpeg

import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''

def main():
    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
    mnist = input_data.read_data_sets(data_path, one_hot=True)
    full_data_x = mnist.train.images

    # total steps to train
    num_steps = 200
    # number of per batch
    batch_size = 1024
    # number of clusters
    k = 25
    # the 10 digits
    num_classes = 10
    # each image is 28*28 pixels
    num_features = 784

    # input images
    X = tf.placeholder(tf.float32, shape=[None, num_features])
    # Lables (for assigning a label to a centroid and testing)
    Y = tf.placeholder(tf.float32, shape=[None, num_classes])

    kmeans = KMeans(inputs=X,num_clusters=k, distance_metric='cosine', use_mini_batch=True)

    train_graph = kmeans.training_graph()

    if len(train_graph) > 6:
        (all_scores, cluster_idx, scores, cluster_centers_initialized, cluster_centers_var, init_op, train_op) = train_graph
    else:
        (all_scores, cluster_idx, scores, cluster_centers_initialized, init_op, train_op) = train_graph

    cluster_idx = cluster_idx[0]
    avg_distance = tf.reduce_mean(scores)

    with tf.Session() as sess:
        init = tf.global_variables_initializer()
        # run the initializer
        sess.run(init, feed_dict={X:full_data_x})
        sess.run(init_op, feed_dict={X:full_data_x})

        for i in range(num_steps):
            _,d,idx = sess.run([train_op, avg_distance, cluster_idx], feed_dict={X:full_data_x})
            if i % 10 == 0:
                print("step {0} avg distance: {1}".format(i, d))

        # assign a label to each centroid
        # count total number of labels per centroid, using the label of each training
        # sample to their closest centroid
        counts = np.zeros(shape=(k, num_classes))
        for i in range(len(idx)):
            counts[idx[i]] += mnist.train.labels[i]
        # assign the most frequent label to the centroid
        labels_map = [np.argmax(c) for c in counts]
        labels_map = tf.convert_to_tensor(labels_map)

        # evaluation ops
        cluster_label = tf.nn.embedding_lookup(labels_map, cluster_idx)
        # computer accuracy
        correct_prediction = tf.equal(cluster_label, tf.cast(tf.argmax(Y, 1), tf.int32))
        accuracy_op = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        test_x, test_y = mnist.test.images, mnist.test.labels
        print('test accuracy : ', sess.run(accuracy_op, feed_dict={X:test_x, Y:test_y}))

if __name__ == '__main__':
    main()
