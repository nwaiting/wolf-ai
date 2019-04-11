#coding=utf-8


"""
    批量并行地进行特征二值化：
        OneHotEncoder：
            将具有多个类别的特征转换为多维二元特征，所有二元特征互斥，当某个二元特征为 1 时，表示取某个类别
            OneHotEncoder(n_values=’auto’, categorical_features=’all’, dtype=<class ‘numpy.float64’>, sparse=True, handle_unknown=’error’)
                sparse : boolean, default=True
                    Will return sparse matrix if set True else will return an array.
            OneHotEncoder无法直接对字符串型的类别变量编码，如何对字符类型进行变量编码：
                方法一 先用 LabelEncoder() 转换成连续的数值型变量，再用 OneHotEncoder() 二值化
                方法二 直接用 LabelBinarizer() 进行二值化
            原因是 sklearn 的新版本中，OneHotEncoder 的输入必须是 2-D array，而 testdata.age 返回的 Series 本质上是 1-D array，所以要改成
                OneHotEncoder(sparse = False).fit_transform( testdata[['age']] )
            结果中哪几列属于 age 的二值化编码，哪几列属于 salary 的，这时候我们可以通过 OneHotEncoder() 自带的 feature_indices_ 来实现这一要求，比如这里 feature_indices_ 的值是[0, 3, 6]，表明 第[0:3]列是age的二值化编码，[3:6]是salary的

        LabelBinarizer：
            和 OneHotEncoder 类似，将类别特征转换为多维二元特征，并将每个特征扩展成用一维表示
            主要是将多类标签转化为二值标签，最终返回的是一个二值数组或稀疏矩阵
            参数说明：
                neg_label：输出消极标签值
                pos_label：输出积极标签值
                sparse_output：设置True时，以行压缩格式稀疏矩阵返回，否则返回数组
                classes_属性：类标签的取值组成数组
        LabelEncoder：
            将类别特征标记为 0 到 n_classes - 1 之间的编码
        MultiLabelBinarizer：
            和 LabelBinarizer 类似
"""

import pandas as pd
from sklearn.preprocessing import OneHotEncoder,LabelEncoder,LabelBinarizer,MultiLabelBinarizer,Binarizer



def f1():
    pass


def f2():
    le = LabelEncoder()
    le.fit([1, 2, 2, 6])
    print(le.classes_)  # [1 2 6]
    print(le.transform([1, 1, 2, 6]))   #[0 0 1 2]

def f3():
    lb = LabelBinarizer(neg_label=2,pos_label=4)
    lb.fit([1, 2, 6, 4, 2])
    res = lb.transform([1, 2, 6, 4, 2])
    """
        1转换成[4, 2, 2, 2]，由于标签有4个值，因此用4位表示，生成[4, 2, 2, 2]的顺序，是按照数据与classes_属性获取的数组顺序匹配的，
        出现的位置为pos_label值，其他位置为neg_label值，通过下面测试集再验证该逻辑
    """
    print(res)
    print(lb.classes_)

def f4():
    mlb = MultiLabelBinarizer()
    res = mlb.fit_transform([(1, 2), (3,4),(5,)])
    print(res)
    print(mlb.classes_)














if __name__ == '__main__':
    f1()
    #f2()
    f3()
    #f4()
