#coding=utf-8

import gensim
import numpy as np

#词集合分布
vocab = ['money','loan','bank','river','stream']
z_1 = np.array([1/3,1/3,1/3,0,0]) #
z_2 = np.array([0,0,1/3,1/3,1/3])
#对应的ψ矩阵  主题-word 分布
phi_actual = np.array([z_1,z_2]).T.reshape(len(z_2), 2)
print(phi_actual)

#生成模型 用之前的分布生成文章 然后用生成的文章进行学习
#用之前的分布生成16个文档
D = 16
#每个文档的长度
mean_length = 10
#根据泊松分布，每个不同的文档句子的长度
len_doc = np.random.poisson(mean_length, size=D)
#两个主题
T = 2
#从概率分布中抽取单词组成句子
docs = []
orig_topics = []
for i in range(D):
    z = np.random.randint(0,2)
    if z == 0:
        words = np.random.choice(vocab, size=[len_doc[i]], p=z_1).tolist()
    else:
        words = np.random.choice(vocab, size=[len_doc[i]], p=z_2).tolist()
    orig_topics.append(z)
    docs.append(words)
print(docs)
print(orig_topics)

#猜测概率分布 学习过程
# 第一步 随机初始化参数 准备学习
w_i = [] #单词
i = []
d_i = [] #文档
z_i = [] #主题
counter = 0
for doc_index,doc in enumerate(docs):
    for word_index,word in enumerate(doc):
        #找到单词在总集合中的位置
        w_i.append(np.where(np.array(vocab)==word)[0][0])
        i.append(counter)
        d_i.append(doc_index)
        #初始化topic分布
        z_i.append(np.random.randint(0,T))
        counter += 1
w_i = np.array(w_i)
d_i = np.array(d_i)
z_i = np.array(z_i)

#第二步 初始化参数θd和ψt
#word-topic 矩阵
WT = np.zeros((len(vocab), T))
for idx,word in enumerate(vocab):
    # 每一个单词下的topic进行计数
    topics = z_i[np.where(w_i==idx)]
    print('topics ', topics)
    for t in range(T):
        WT[idx,t] = sum(topics==t)

#doc-topic 矩阵
DT = np.zeros((D,T))
for idx,doc in enumerate(docs):
    #对每个话题，这个句子服从它的次数
    topics = z_i[np.where(d_i==idx)]
    for t in range(T):
        DT[idx,t] = sum(topics==t)

#第三步：
WT_origin = WT.copy()
DT_origin = DT.copy()

#采集记录仪 记录每一个phi的变化结果
phi_1 = np.zeros((len(vocab), 100))
phi_2 = np.zeros((len(vocab), 100))

#共跑100次
iters = 100

#安排一个Dirichlet先验分布（通过参数），有a,b两个参数，通过参数进行控制
alpha = 1
beta = 1

for step in range(iters):
    for current in i:
        #把D好玩W分别拿出来
        doc_idx = d_i[current]
        word_idx = w_i[current]

        #从集合中删除
        DT[doc_idx, z_i[current]] -= 1
        WT[word_idx, z_i[current]] -= 1

        #计算新的W和D的分布
        prob_word = (WT[word_idx,:] + beta)/(WT[:,:].sum(axis=0) + len(vocab)*beta)
        prob_document = (DT[doc_idx,:] + alpha)/(DT[:,:].sum(axis=0) + D*alpha)
        #对于每一个topic的概率
        prob = prob_word * prob_document

        #更新z 根据概率
        z_i[current] = np.random.choice([0,1], 1, p=prob/prob.sum())[0]

        #更新计数器
        DT[doc_idx, z_i[current]] += 1
        WT[word_idx, z_i[current]] += 1

        #记录phi的变化 计算后验值
        phi = WT/(WT.sum(axis=0))
        phi_1[:,step] = phi[:,0]
        phi_2[:,step] = phi[:,1]

#统计
theta = DT/DT.sum(axis=0)
#归一
theta = theta/np.sum(theta, axis=1).reshape(16,1)
#验证 最后分类结果和初始结果的比较
np.argmax(theta, axis=1) == orig_topics

def main():
    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    lda = gensim.models.ldamodel.LdaModel(corpus=None, id2id2word=None, num_topics=20)
    lda.get_document_topics(bow=None)
    lda.get_term_topics(word_id=None)
