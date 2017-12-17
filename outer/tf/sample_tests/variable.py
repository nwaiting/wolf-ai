#coding=utf8

import tensorflow as tf

def main():
    state = tf.Variable(0, name='counter')
    one = tf.constant(1)
    new_value = tf.add(state, one)
    update = tf.assign(state, new_value)
    #init = tf.initialize_all_variables()
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        for _ in range(3):
            sess.run(update)
            print(sess.run(state))

if __name__ == '__main__':
    main()
