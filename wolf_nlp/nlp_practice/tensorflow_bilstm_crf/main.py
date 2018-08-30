#coding=utf-8
import os
import time
import tensorflow as tf
import numpy as np
from model import BiLSTM_CRF
from text_handler import TextHandler, read_dictionary, random_embedding, read_corpus, tag2label, get_entiry

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
tf.flags.DEFINE_string('mode', 'demo', 'train/test/demo')
tf.flags.DEFINE_string('demo_model', '1521112368', 'model for test and demo')

FLAGS = tf.flags.FLAGS

os.environ['CUDA_VISIBLE_DEVICES'] = '-1' #禁用GPU
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #tf log level default 0

config = tf.ConfigProto()

def main(_):
    print('start app')

    data_path = os.path.join(FLAGS.train_data, 'word2id.pkl')
    word2id = read_dictionary(data_path)
    if FLAGS.pretrain_embedding == 'random':
        data_embeddings = random_embedding(word2id, FLAGS.embedding_dim)
    else:
        embedding_path = 'pretrain_embedding.npy'
        data_embeddings = np.array(np.load(embedding_path), dtype='float32')

    if FLAGS.model != 'demo':
        train_file = os.path.join(FLAGS.train_data, 'train_data')
        test_file = os.path.join(FLAGS.test_data, 'test_data')
        train_data = read_corpus(train_file)
        test_data = read_corpus(test_file)
        test_size = len(test_data)

    time_stamp = str(int(time.time())) if FLAGS.mode == 'train' else FLAGS.demo_model
    def generator_dir(file_path):
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        return file_path
    output_path = generator_dir(os.path.join(FLAGS.train_data + '_save', time_stamp))
    summary_path = generator_dir(os.path.join(output_path, 'summary'))
    model_path = generator_dir(os.path.join(output_path, 'checkpoints'))
    ckpt_prefix = generator_dir(os.path.join(model_path, 'model'))
    result_path = generator_dir(os.path.join(output_path, 'results'))

    if FLAGS.mode == 'train':
        print('train ==================')
        """
        def __init__(self, batch_size, epoch, hidden_size, embeddings, crf, update_embedding, dropout_keepprob, optimizer,
         learning_rate, clip, tag2label, vocab, shuffle, model_p, summary_p, results_p, config):
        """
        model = BiLSTM_CRF(FLAGS.batch_size,
                            FLAGS.epoch,
                            FLAGS.hidden_size,
                            data_embeddings,
                            FLAGS.crf,
                            FLAGS.update_embedding,
                            FLAGS.dropout_keepprob,
                            FLAGS.optimizer,
                            FLAGS.learning_rate,
                            FLAGS.clip,
                            tag2label,
                            word2id,
                            FLAGS.shuffle,
                            model_path,
                            summary_path,
                            result_path,
                            config)
        model.build_graph()
        model.train(train_data, test_data)
    elif FLAGS.mode == 'test':
        print('test ===============')
        ckpt_file = tf.train.latest_checkpoint(model_path)
        print('ckpt file {}'.format(ckpt_file))
        model = BiLSTM_CRF(FLAGS.batch_size,
                            FLAGS.epoch,
                            FLAGS.hidden_size,
                            data_embeddings,
                            FLAGS.crf,
                            FLAGS.update_embedding,
                            FLAGS.dropout_keepprob,
                            FLAGS.optimizer,
                            FLAGS.learning_rate,
                            FLAGS.clip,
                            tag2label,
                            word2id,
                            FLAGS.shuffle,
                            ckpt_file,
                            summary_path,
                            result_path,
                            config)
        model.build_graph()
        print('test data {}'.format(test_size))
        model.test(test_data)
    elif FLAGS.mode == 'demo':
        print('demo ===========')
        ckpt_file = tf.train.latest_checkpoint(model_path)
        print('ckpt file {}'.format(ckpt_file))
        model = BiLSTM_CRF(FLAGS.batch_size,
                            FLAGS.epoch,
                            FLAGS.hidden_size,
                            data_embeddings,
                            FLAGS.crf,
                            FLAGS.update_embedding,
                            FLAGS.dropout_keepprob,
                            FLAGS.optimizer,
                            FLAGS.learning_rate,
                            FLAGS.clip,
                            tag2label,
                            word2id,
                            FLAGS.shuffle,
                            ckpt_file,
                            summary_path,
                            result_path,
                            config)
        model.build_graph()
        saver = tf.train.Saver()
        with tf.Session(config=config) as sess:
            saver.restore(sess, ckpt_file)
            while True:
                print("please input you sentence:")
                demo_sentence = input()
                if not demo_sentence or demo_sentence.isspace():
                    print('bye')
                    break
                else:
                    demo_sent = list(demo_sentence.strip())
                    damo_data = [(demo_sent, [0] * len(demo_sent))]
                    tag = model.demo_one(sess, damo_data)
                    per,loc,org = get_entiry(tag, demo_sent)
                    print('per {0} loc {1} org {2}'.format(per, loc, org))

if __name__ == '__main__':
    tf.app.run()
