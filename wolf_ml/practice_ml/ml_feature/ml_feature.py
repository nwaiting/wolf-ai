# coding=utf-8


"""
    参考：https://github.com/HanXiaoyang/Kaggle_Titanic
        https://blog.csdn.net/han_xiaoyang/article/details/49797143
        http://www.cnblogs.com/jasonfreak/p/5448385.html

    总结的一些经验：
        baseline model：
            Andrew Ng老师似乎在coursera上说过，应用机器学习，千万不要一上来就试图做到完美，先撸一个baseline的model出来，
            再进行后续的分析步骤，一步步提高，所谓后续步骤可能包括『分析model现在的状态(欠/过拟合)，分析我们使用的feature的作用大小，
            进行feature selection，以及我们模型下的bad case和产生的原因』等等

        特征处理：
            Kaggle上的大神们，也分享过一些experience，说几条我记得的哈：
            『对数据的认识太重要了！』
            『数据中的特殊点/离群点的分析和处理太重要了！』
            『特征工程(feature engineering)太重要了！在很多Kaggle的场景下，甚至比model本身还要重要』
            『要做模型融合(model ensemble)啊啊啊！』


"""

from sklearn.model_selection import train_test_split


def main():
    pass


if __name__ == '__main__':
    main()
