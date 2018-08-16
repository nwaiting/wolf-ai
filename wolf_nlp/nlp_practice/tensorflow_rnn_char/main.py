#coding=utf-8
import os
import tensorflow as tf
from text_parse import TextHandler
from model import RNNChar

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
tf.flags.DEFINE_float('training_keep_prob', 0.9, 'dropout rate during training')
tf.flags.DEFINE_integer('grad_clip', 5, 'grad_clip')
tf.flags.DEFINE_integer('max_steps', 5000, 'max train steps')
tf.flags.DEFINE_integer('max_vocab', 3500, 'max char number')
tf.flags.DEFINE_string('input_file', '', 'utf8 text file for train')

#example prams
tf.flags.DEFINE_string('vocab_load_file', '', 'load vocab file path')
tf.flags.DEFINE_string('vocab_save_file', '', 'save vocab file path')
tf.flags.DEFINE_string('checkpoint_file', '', 'checkpoint path')
tf.flags.DEFINE_string('start_string', '', 'string to start generate text')
tf.flags.DEFINE_integer('max_length', 100, 'max char to generate')

# statistics prams
tf.flags.DEFINE_integer('save_every_step', 1000, 'save the model every 1000 steps')
tf.flags.DEFINE_integer('log_every_step', 100, 'log the statistics every 100 steps')

FLAGS = tf.flags.FLAGS

def main(_):
    current_path = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.dirname(FLAGS.model_name)
    model_path = os.path.join(current_path, model_path)
    if not os.path.exists(model_path):
        try:
            os.makedirs(model_path)
        except Exception as e:
            print('create dir error {0}'.format(e))

    texts = TextHandler(file=FLAGS.input_file,
                        max_vocab=FLAGS.max_vocab,
                        vocab_load_file=FLAGS.vocab_load_file,
                        time_inputs=FLAGS.time_inputs,
                        time_steps=FLAGS.time_steps,
                        vocab_save_file=FLAGS.vocab_save_file
                        )

    """
    time_steps=28,
    time_inputs=28,
    hidden_size=128,
    num_layers=2,
    learning_rate=0.001
    grad_clip=5,
    sampling=False,
    training_keep_prob=0.5,
    use_embedding=False,
    embedding_size=300,
    model_path = None,
    max_steps = 10000,
    save_every_step = 1000,
    log_every_step = 100
    """
    model = RNNChar(texts.vocab_size,
                    time_steps=FLAGS.time_steps,
                    time_inputs=FLAGS.time_inputs,
                    hidden_size=FLAGS.hidden_size,
                    num_layers=FLAGS.num_layers,
                    learning_rate=FLAGS.learning_rate,
                    grad_clip=FLAGS.grad_clip,
                    sampling=FLAGS.type == 'example',
                    training_keep_prob=FLAGS.training_keep_prob,
                    use_embedding=FLAGS.use_embedding,
                    embedding_size=FLAGS.embedding_size,
                    model_path=model_path,
                    max_steps=FLAGS.max_steps,
                    log_every_step=FLAGS.log_every_step,
                    save_every_step=FLAGS.save_every_step
                    )
    if FLAGS.type == 'example':
        model.load(os.path.join(model_path, FLAGS.checkpoint_file))
        model.example(FLAGS.max_length, '', texts.vocab_size)
    elif FLAGS.type == 'train':
        model.train(texts.get_batch())

if __name__ == "__main__":
    tf.app.run()
