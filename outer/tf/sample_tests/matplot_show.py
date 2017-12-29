#coding=utf-8

import matplotlib.pyplot as plt
import tensorflow as tf

def main():
    x_data = tf.Variable(tf.random_normal([100], dtype=tf.float32))
    y_data = tf.add(tf.multiply(x_data, 0.3) , 0.5)
    with tf.Session() as sess:
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        #ax.scatter(sess.run(x_data), sess.run(y_data))
        ax.plot(sess.run(x_data), sess.run(y_data), 'r')
        #plt.plot(sess.run(x_data), sess.run(y_data), 'ro')
        #plt.legend()
        plt.show()

if __name__ == '__main__':
    main()
