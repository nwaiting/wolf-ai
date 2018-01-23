#coding=utf-8

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

# TensorFlow集群描述信息，ps_hosts表示参数服务节点信息，worker_hosts表示worker节点信息
"""
    worker和server
    worker负责计算
    server负责更新模型参数
"""
tf.app.flags.DEFINE_string("ps_hosts", "127.0.0.1:2222,128.0.0.1:2222,129.0.0.1:2222", "Comma-separated list of hostname:port pairs")
tf.app.flags.DEFINE_string("worker_hosts", "127.0.0.2:2222", "Comma-separated list of hostname:port pairs")

# TensorFlow Server模型描述信息，包括作业名称，任务编号，隐含层神经元数量，MNIST数据目录以及每次训练数据大小（默认一个批次为100个图片）
tf.app.flags.DEFINE_string("job_name", "", "One of 'ps', 'worker'")
tf.app.flags.DEFINE_integer("task_index", 0, "Index of task within the job")
tf.app.flags.DEFINE_integer("hidden_units", 100, "Number of units in the hidden layer of the NN")
tf.app.flags.DEFINE_string("data_dir", "MNIST_data", "Directory for storing mnist data")
tf.app.flags.DEFINE_integer("batch_size", 100, "Training batch size")

FLAGS = tf.app.flags.FLAGS
#图片像素大小为28*28像素
IMAGE_PIXELS = 28

def main():
    ps_hosts = FLAGS.ps_hosts.split(',')
    worker_hosts = FLAGS.worker_hosts.split(',')

    #创建集群对象
    cluster = tf.train.ClusterSpec({'ps':ps_hosts, 'worker':worker_hosts})
    #本地执行task，创建本地Server对象
    server = tf.train.Server(cluster, job_name=FLAGS.job_name, task_index=FLAGS.task_index)
    if FLAGS.job_name == 'ps':
        server.join()
    elif FLAGS.job_name == 'worker':
        with tf.device(tf.train.replica_device_setter(worker_device="/job:worker/task:{0}".format(FLAGS.task_index), cluster=cluster)):
            #定义隐层参数变量，为全连接神经网络隐层
            hid_w = tf.Variable(tf.truncated_normal([IMAGE_PIXELS*IMAGE_PIXELS, FLAGS.hidden_units], stddev=1.0/IMAGE_PIXELS), name='hid_w')
            hid_b = tf.Variable(tf.zeros([FLAGS.hidden_units]), name='hid_b')

            #定义softmax回归层的参数
            sm_w = tf.Variable(tf.truncated_normal([FLAGS.hidden_units, 10], stddev=1.0/tf.sqrt(FLAGS.hidden_units)), name='sm_w')
            sm_b = tf.Variable(tf.zeros(10), name='sm_b')

            #定义模型输入
            x = tf.placeholder(tf.float32, [None, IMAGE_PIXELS*IMAGE_PIXELS])
            y_ = tf.placeholder(tf.float32, [None, 10])

            #定义隐层及神经元计算模型
            hid_lin = tf.nn.xw_plus_b(x, hid_w, hid_b)
            hid = tf.nn.relu(hid_lin)

            #定义softmax模型和损失函数
            y = tf.nn.softmax(tf.nn.xw_plus_b(x, sm_w, sm_b))
            loss = -tf.reduce_mean(y_ * tf.log(tf.clip_by_value(y, 1e-10, 1.0)))

            #定义全局步长
            global_step = tf.Variable(0)
            #定义训练模型 采用Adagrad梯度下降法
            train_optimizer = tf.train.AdagradOptimizer(0.01).minimize(loss=loss, global_step=global_step)

            #定义模型精确度验证模型 统计模型精确度
            correct_predict = tf.equal(tf.argmax(y,1), tf.argmax(y,1))
            accuracy = tf.reduce_mean(tf.cast(correct_predict, tf.float32))

            #对模型定期checkpoint，通常用于模型恢复
            saver = tf.train.Saver()

            #定期收集模型的统计信息
            summary_optimizer = tf.merge_all_summaries()

            #初始化所有模型变量
            init_optimizer = tf.global_variables_initializer()

            #创建一个监管程序 用于构建模型检查点以及计算模型统计信息
            sv = tf.train.Supervisor(is_chief=(FLAGS.task_index==0), logdir='/tmp/train_logs', init_op=init_optimizer, summary_op=summary_optimizer, saver=saver, global_step=global_step, save_model_secs=600)

            minist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True)

            with sv.managed_session(server.target) as sess:
                step = 0
                while not sv.should_stop() and step < 1000:
                    batch_xs, batch_ys = minist.train.next_batch(FLAGS.batch_size)

                    #执行分布式的模型训练
                    _,step = sess.run([train_optimizer, global_step], feed_dict={x:batch_xs,y:batch_ys})

                    #每隔多少步验证
                    if step % 100 == 0:
                        print('done step {0}'.format(step))
                        print(sess.run(accuracy, feed_dict={x:minist.test.images, y_:minist.test.labels}))
            sv.stop()

if __name__ == '__main__':
    #main()
    tf.app.run()
