## NLP_总结 -- word2vec vs fasttext
- **概述：**
>
>
>
>
>
>
>
>

### word2vec：
- **网络结构：**
>       先构造一个权重矩阵W1，然后通过对单词进行hash找到W1(大小为[v,n])所对应的某一行的向量，此向量即为word embedding的向量，
>           然后通过隐层的向量与权重W2(大小为[n,v])进行计算，得到输出向量O,通过对向量O做一个softmax多分类，即可算法每个词出现的概率
>
>       更新权重：
> ![avatar](https://github.com/nwaiting/wolf-ai/blob/master/wolf_others/pic/word2vec_weights_update.png)
>
>

- **CBOW和Skip-Gram：**
>       CBOW：
>           1、通过对周围的词的向量进行加权求取平均值向量，这个平均值向量即为隐层向量的输出，然后和权重矩阵W2进行计算，最后的进行softmax进行多分类
>               训练CBOW时，由于输入是上下文的词向量，需要对输入词向量求平均得到隐层输出向量，然后进行W2的计算
>           2、训练Skip-Gram向量时，选定窗口大小window，对每个词生成2*window个训练样本，注意batch_size的大小必须是2*window的整数倍，确保每个batch包含一个词汇对应的所有样本
>           3、对小型数据集比较适合
>
> ![avatar](https://github.com/nwaiting/wolf-ai/blob/master/wolf_others/pic/word2vec_cbow.png)
>
>       Skip-Gram：
>           1、由于输入是一个词向量，所以不需要进行平均
>           2、训练Skip-Gram向量时，选定窗口大小window，对每个词生成2*window个训练样本，注意batch_size的大小必须是2*window的整数倍，确保每个batch包含一个词汇对应的所有样本
>           3、对大语料比较适合
>

- **word2vec的优化：**
>       1、subsamping
>           对每个词按照一定的概率进行保留或者丢弃
> 
>       2、Negative Sampling
>           负采样，没有采用霍夫曼树，每次只是通过采样neg个不同的中心词做负例，就可以训练模型了。
>
>       3、Hierarchical Softmax
>           采用霍夫曼树代替传统的训练方法，可以提高模型训练效率。
>           如果样本中有一个生僻词，那么在霍夫曼树中就要进行深度的搜索，效率不高。这种情况下，使用负采样效率较高。
>           将V分类问题优化成了log(V)次二分类问题，Hierarchical Softmax只是softmax的一种近似形式
>           详解：
>               最先优化和使用的数据结构是用霍夫曼树来代替隐层和输出层的神经元。霍夫曼树的叶子结点起到输出神经元的作用，叶子结点即词汇表的大小。
>               而内部节点则起到隐层神经元的作用。
>
>
>
>

- **霍夫曼编码：**
>       霍夫曼树的构造：
>           1、看做是n颗树的森林，每一棵树仅有一个节点
>           2、对所有的树进行合并
>
>       约定编码：
>           可以约定如左子树编码为1，右子树编码为0，则可以对任一叶子节点进行01编码
>
>
>
>

- **待续：**
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
