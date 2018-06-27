#coding=utf-8

from functools import reduce

"""
    手写一个感知器
"""

class Perceptron(object):
    def __init__(self, in_num, activation=None):
        """
            @in_num 输入参数个数
            @activation 激活函数 类型为double->double
        """
        self.activation_ = self.f
        if activation:
            self.activation_ = activation
        self.weights_ = [0.0 for _ in range(in_num)]
        self.bias_ = 0.0

    def __str__(self):
        """
            打印学习的权重和偏置
        """
        return 'weights : {0} bias: {1:.3f}'.format(self.weights_, self.bias_)

    def predict(self, in_vec):
        """
            预测结果
            y = W*X + b
        """
        pre_value = reduce(lambda a,b:a+b, map(lambda x,w:x*w, in_vec,self.weights_), 0.0) + self.bias_
        return self.activation_(pre_value)

    def train(self, in_vec, labels, epoch, l_rate):
        """
            训练
            @in_vec：输入数据向量
            @labels：每个向量对应的label
            @epoch：训练轮数
            @l_rate：学习率
        """
        for i in range(epoch):
            self.one_epoch(in_vec, labels, l_rate)

    def one_epoch(self, in_vec, labels, l_rate):
        """
            单次训练
            @in_vec：输入数据向量
            @labels：每个向量对应的label
            @l_rate：学习率
        """
        samples = zip(in_vec, labels)
        for in_vec,label in samples:
            output = self.predict(in_vec)
            self.update_weights(in_vec, output, label, l_rate)

    def update_weights(self, in_vec, output, label, l_rate):
        """
            更新权重
        """
        print('label ', label, output)
        delta = label - output
        # ▽Wi = η(t - y)xi
        self.weights_ = list(map(lambda x,w:x+l_rate*delta*x, in_vec, self.weights_))
        # ▽b = η(t - y)
        self.bias_ = self.bias_ + delta * l_rate


    def f(self, x):
        """
            激活函数
        """
        return 1 if x > 0 else 0


def get_train_data():
    """
        构建一个and感知器的训练数据
    """
    in_vec = [[1,1], [0,0], [1,0], [0,1],[1,1], [0,0], [1,0], [0,1],[1,1], [0,0], [1,0], [0,1],[1,1], [0,0], [1,0], [0,1]]
    labels = [1, 0, 0, 0,1, 0, 0, 0,1, 0, 0, 0,1, 0, 0, 0]
    return in_vec,labels

def train_and_perceptron():
    """
        训练一个and感知器
    """
    p = Perceptron(2)
    in_vec,labels = get_train_data()
    p.train(in_vec, labels, 1000, 0.01)
    return p


if __name__ == '__main__':
    and_preceptron = train_and_perceptron()
    print(and_preceptron)
    print('1 and 1 = {0}'.format(and_preceptron.predict([1,1])))
    print('1 and 0 = {0}'.format(and_preceptron.predict([1,0])))
    print('0 and 1 = {0}'.format(and_preceptron.predict([0,1])))
    print('0 and 0 = {0}'.format(and_preceptron.predict([0,0])))
