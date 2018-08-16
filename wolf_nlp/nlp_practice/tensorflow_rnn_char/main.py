#coding=utf-8
import os
import tensorflow as tf
from text_parse import TextHandler

tf.flags.DEFINE_string('type', 'example', 'do what train or example')
tf.flags.DEFINE_string('model_name', '', 'model name with path')

#train prams
tf.flags.DEFINE_integer('time_steps', 28, 'number of steps in one batch')
tf.flags.DEFINE_integer('time_inputs', 28, 'length of time_steps')
tf.flags.DEFINE_integer('hidden_size', 128, 'lstm hidden size')
tf.flags.DEFINE_integer('num_layers', 2, 'number of lstm layers')
tf.flags.DEFINE_bool('use_embedding', False, 'use embedding or not')
tf.flags.DEFINE_integer('embedding_size', 300, 'size of embedding')
tf.flags.DEFINE_float('learning_rate', 0.001, 'learning rate')
tf.flags.DEFINE_float('train_keep_prob', 0.5, 'dropout rate during training')
tf.flags.DEFINE_integer('max_steps', 5000, 'max train steps')
tf.flags.DEFINE_integer('max_vocab', 3500, 'max char number')
tf.flags.DEFINE_string('train_file', '', 'utf8 text file for train')

#example prams
tf.flags.DEFINE_string('vocab_load_file', '', 'load vocab file path')
tf.flags.DEFINE_string('vocab_save_file', '', 'save vocab file path')
tf.flags.DEFINE_string('checkpoint_path', '', 'checkpoint path')
tf.flags.DEFINE_string('start_string', '', 'string to start generate text')
tf.flags.DEFINE_integer('max_length', 100, 'max char to generate')

# statistics prams
tf.flags.DEFINE_integer('save_every_step', 1000, 'save the model every 1000 steps')
tf.flags.DEFINE_integer('log_every_step', 100, 'log the statistics every 100 steps')

FLAGS = tf.flags.FLAGS

def main(_):
    model_path = os.path.dirname(FLAGS.model_name)
    if not os.path.exists(model_path):
        try:
            os.makedirs(model_path)
        except Exception as e:
            print('create dir error {0}'.format(e))

    texts = TextHandler(file=FLAGS.input_file,
                        max_vocab=FLAGS.max_vocab,
                        vocab_load_file=os.path.join(model_path, FLAGS.vocab_load_file),
                        time_inputs=FLAGS.time_inputs,
                        time_steps=FLAGS.time_steps,
                        vocab_save_file=os.path.join(model_path, FLAGS.vocab_save_file)
                        )
    
    if FLAGS.type == 'example':
        pass
    elif FLAGS.type == 'train':
        pass


if __name__ == "__main__":
    tf.app.run()
