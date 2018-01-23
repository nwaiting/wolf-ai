#coding=utf8

import tensorflow as tf

def main():
    input1 = tf.placeholder(tf.float32)
    input2 = tf.placeholder(tf.float32)
    output = tf.multiply(input1, input2)

    with tf.Session() as sess:
        print(sess.run(output, feed_dict={input1:[3.], input2:[7.]}))

if __name__ == '__main__':
    main()
