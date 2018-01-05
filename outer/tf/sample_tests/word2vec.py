#coding=utf-8
# https://github.com/nlintz/TensorFlow-Tutorials/blob/master/08_word2vec.ipynb

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import collections

def main():
    batch_size = 20
    # dimension of the embedding vector. two too small to get
    # any meaningful embeddings, but let's make it 2 for simple visualization
    embedding_size = 2
    # number of negative examples to sample
    num_sampled = 15

    contents = ["the quick brown fox jumped over the lazy dog",
            "I love cats and dogs",
            "we all love cats and dogs",
            "cats and dogs are great",
            "sung likes cats",
            "she loves dogs",
            "cats can be very independent",
            "cats are great companions when they want to be",
            "cats are playful",
            "cats are natural hunters",
            "It's raining cats and dogs",
            "dogs and cats love sung"]
    words = " ".join(contents).split()
    # 返回的是一个对象
    # counts = collections.Counter(words)
    # 返回的是词频列表
    counts = collections.Counter(words).most_common()
    print(counts)

    # idx -> word
    rdic = [i[0] for i in counts]
    # word -> id
    vector_dic = {w:i for i,w in enumerate(rdic)}
    voc_size = len(vector_dic)

    data = [vector_dic[word] for word in words]
    print('data ', data[:5])

    # make a training data
    # ([the, brown], quick), ([quick, fox], brown), ([brown, jumped], fox)
    cbow_pairs = []
    for i in range(1, len(data) - 1):
        cbow_pairs.append([[data[i-1], data[i+1]], data[i]])
    print(cbow_pairs[:5])

    # make skip-gram pairs
    # (quick, the), (quick, brown), (brown, quick), (brown, fox)
    skip_gram_pairs = []
    for c in cbow_pairs:
        skip_gram_pairs.append([c[1], c[0][0]])
        skip_gram_pairs.append([c[1], c[0][1]])
    print(skip_gram_pairs[0:5])

    def generate_batch(size):
        x_data,y_data = [],[]
        r = np.random.choice(range(len(skip_gram_pairs)), size=size, replace=False)
        for i in r:
            # n dim
            x_data.append(skip_gram_pairs[i][0])
            # n, 1 dim
            y_data.append([skip_gram_pairs[i][1]])
        return x_data,y_data
    print('batch (x,y) ', generate_batch(3))

    train_inputs = tf.placeholder(tf.int32, shape=[batch_size])
    train_labels = tf.placeholder(tf.int32, shape=[batch_size, 1])
    # 指定操作的设备，设备可以本地的CPU或者GPU，也可以是某一台远程的服务器
    with tf.device('/cpu:0'):
        embeddings = tf.Variable(tf.random_uniform([voc_size, embedding_size], -1., 1., dtype=tf.float32))
        embed = tf.nn.embedding_lookup(embeddings, train_inputs)

    nce_weights = tf.Variable(tf.random_uniform([voc_size, embedding_size], -1., 1., dtype=tf.float32))
    nce_biases = tf.Variable(tf.zeros([voc_size]))

    loss = tf.reduce_mean(tf.nn.nce_loss(nce_weights, nce_biases, train_labels, embed, num_sampled, voc_size))
    optimizer = tf.train.AdamOptimizer(1.0e-1).minimize(loss=loss)

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for step in range(1000+1):
            batch_inputs,batch_labels = generate_batch(batch_size)
            _,loss_val = sess.run([optimizer,loss], feed_dict={train_inputs:batch_inputs, train_labels:batch_labels})
            if step % 20 == 0:
                print("{0} {1}".format(step, loss_val))
        training_embeddings = embeddings.eval()

    if training_embeddings.shape[1] == 2:
        labels = rdic[:10] # top 10
        for i,label in enumerate(labels):
            x,y = training_embeddings[i,:]
            print('x,y',x,y)
            plt.scatter(x, y)
            plt.annotate(label, xy=(x,y), xytext=(5,2), textcoords='offset points', ha='right', va='bottom')
        plt.show()
        #plt.savefig('word2vec.png')

if __name__ == '__main__':
    main()
