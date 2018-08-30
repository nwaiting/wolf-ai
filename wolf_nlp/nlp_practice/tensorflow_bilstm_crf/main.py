#coding=utf-8

import tensorflow as tf
from text_handler import TextHandler

'''
    BiLSTM-CRF Chinese NER task
'''

tf.flags.DEFINE_string('train_data', 'data_path', 'train data source')
tf.flags.DEFINE_string('test_data', 'data_path', 'test data source')
tf.flags.DEFINE_integer('batch_size', 128, 'sample of each minibatch')
tf.flags.DEFINE_integer('epoch', 50, 'epoch of training')
tf.flags.DEFINE_integer('hidden_size', 128, 'dim of hidden size')
tf.flags.DEFINE_string('optimizer', 'Adam', 'Adam/Adadelta/Adagrad/RMSProp/Momentum/SGD')
tf.flags.DEFINE_boolean('CRF', True, 'use CRF at the top layer,if false, use softmax')
tf.flags.DEFINE_float('learning_rate', 0.001, 'learning rate')
tf.flags.DEFINE_float('clipping', 5.0, 'gradient clipping')
tf.flags.DEFINE_float('dropout', 0.5, 'dropout keep prob')
tf.flags.DEFINE_boolean('update_embedding', True, 'update embedding during training')
tf.flags.DEFINE_string('pretrain_embedding', 'random', 'use pretrain char embedding or init it randomly')
tf.flags.DEFINE_integer('embedding_dim', 300, 'embedding dim')
tf.flags.DEFINE_boolean('shuffle', True, '')
tf.flags.DEFINE_string('model', 'demo', 'train/test/demo')
tf.flags.DEFINE_string('demo_model', '1521112368', 'model for test and demo')

FLAGS = tf.flags.FLAGS

def main(_):
    print('start app')
    text_handler = TextHandler()
    print(tf.__version__)
    a = {'a':0,'b':1}
    for _ in a.items():
        print(_)

if __name__ == '__main__':
    tf.app.run()
