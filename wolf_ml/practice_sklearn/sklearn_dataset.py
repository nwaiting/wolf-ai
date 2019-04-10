#coding=utf-8


"""
    sklearn 的数据集有好多个种
        自带的小数据集（packaged dataset）：sklearn.datasets.load_<name>
        可在线下载的数据集（Downloaded Dataset）：sklearn.datasets.fetch_<name>
        计算机生成的数据集（Generated Dataset）：sklearn.datasets.make_<name>
        svmlight/libsvm格式的数据集:sklearn.datasets.load_svmlight_file(...)
        从买了data.org在线下载获取的数据集:sklearn.datasets.fetch_mldata(...)

    自带的数据集：
        其中的自带的小的数据集为：sklearn.datasets.load_<name>
        load_iris 鸢尾花
        load_breast_cancer  乳腺癌数据
        load_digits 手写数字
        load_diabetes   糖尿病
        load_boston 波士顿房价
        load_linnerud   体能训练

    计算机生成的数据集：
        计算机生成的数据集（Generated Dataset）：sklearn.datasets.make_<name>
        make_blobs  多类单标签数据集，为每个类分配一个或多个正太分布的点集
        make_classification 多类单标签数据集，为每个类分配一个或多个正太分布的点集，提供了为数据添加噪声的方式，包括维度相关性，无效特征以及冗余特征等
        make_gaussian-quantiles 将一个单高斯分布的点集划分为两个数量均等的点集，作为两类
        make_hastie-10-2    产生一个相似的二元分类数据集，有10个维度
        make_circle和make_moom   产生二维二元分类数据集来测试某些算法的性能，可以为数据集添加噪声，可以为二元分类器产生一些球形判决界面的数据

"""

from sklearn.datasets import load_iris,load_breast_cancer,load_digits,load_diabetes,load_boston,load_linnerud
from sklearn.datasets import make_blobs,make_classification,make_gaussian_quantiles,make_hastie_10_2,make_circles,make_moons

def main():
    pass






if __name__ == '__main__':
    main()
