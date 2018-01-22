#coding=utf-8

import tensorflow as tf

tf.nn.avg_pool
tf.layers.Dropout
tf.contrib

"""
TensorFlow 学习笔记：
    tf.nn：
        提供神经网络相关操作的支持，包括卷积操作(conv)，池化操作(pooling)，归一化，loss，分类操作、embedding、RNN、Evaluation
    tf.layers：
        主要提供的高层的神经网络，主要和卷积相关的，感觉是对tf.nn的进一步封装，tf.nn是更底层的操作
    tf.contrib：
        tf.contrib.layers提供能够计算图中的网络层、正则化、摘要操作、是构建计算图的高级操作，但是tf.contrib包含不稳定和实验代码，后面可能会变
        开源社区贡献，新功能，内外部测试，根据分会意见改进性能，改善API友好度，API稳定后，迁移到TensorFlow核心模块
    tf.contrib.ditributions:
        Bernoulli、Beta、Binomial、Gamma、Ecponential、Normal、Poisson、Uniform等统计分布、统计研究、应用中常用，各种统计、机器学习模型基石，概率模型、图形模型依赖
        Gamma分布。contrib.distributions导入Gamma分布，初始化alpha, beta tf.constant()，建立Gamma分布
    layers:
        包含机器学习算法所需要各种成分、部件、卷积层、批标准化层、机器学习指标、优化函数、初始器、特征列
    机器学习层：
        深度学习和计算机视觉二维平均池avg_pool2d
    建立卷积层：
        contrib.layers.convolution2d()建立32个3x3过滤器卷积层
    损失函数：
        tf.contrib.losses模块，各种常用损失函数，二类分类、多类分类、回归模型等机器学习算法
    计算softmax交叉熵：
        多类分类机器学习模型。建立predictions、labels，多给。losses.softmax_cross_entropy()计算预测softmax交叉熵值
    Embeddings：
        嵌入向量。稀疏、高维类别特征向量，转换低维、稠密实数值向量，和连续特征向量联合，一起输入神经网络模型训练和优化损失函数。大部分文本识别，先将文本转换成嵌入向量
    性能分析器tfprof：
        分析模型架构、衡量系统性能。衡量模型参数、浮点运算、op执行时间、要求存储大小、探索模型结构
        tfprof提供两种类型分析：scope、graph。graph，查看op在graph里所花内存、时间
"""

def main():
    pass

if __name__ == '__main__':
    main()
