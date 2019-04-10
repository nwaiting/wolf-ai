# coding=utf-8


"""
    参考：http://www.cnblogs.com/jasonfreak/p/5448462.html

    数据挖掘：
        数据挖掘内容：
            数据挖掘通常包括数据采集，数据分析，特征工程，训练模型，模型评估等步骤。

        特征处理形式有两种：流水线式和并行式。
            基于流水线组合的工作需要依次进行，前一个工作的输出是后一个工作的输入；
            基于并行式的工作可以同时进行，其使用同样的输入，所有工作完成后将各自的输出合并之后输出。
            sklearn提供了包pipeline来完成流水线式和并行式的工作。
            1、并行处理：
                1.1 整体并行处理：
                    pipeline包提供了FeatureUnion类来进行整体并行处理，如下，
                        #新建将整体特征矩阵进行对数函数转换的对象
                        step2_1 = ('ToLog', FunctionTransformer(log1p))
                        #新建将整体特征矩阵进行二值化类的对象
                        step2_2 = ('ToBinary', Binarizer())
                        #新建整体并行处理对象
                        #该对象也有fit和transform方法，fit和transform方法均是并行地调用需要并行处理的对象的fit和transform方法
                        #参数transformer_list为需要并行处理的对象列表，该列表为二元组列表，第一元为对象的名称，第二元为对象
                        step2 = ('FeatureUnion', FeatureUnion(transformer_list=[step2_1, step2_2, step2_3]))

                1.2 部分并行处理：
                    整体并行处理有其缺陷，在一些场景下，我们只需要对特征矩阵的某些列进行转换，而不是所有列。
                    pipeline并没有提供相应的类（仅OneHotEncoder类实现了该功能），需要我们在FeatureUnion的基础上进行优化
                        例如，对特征矩阵的第1列（花的颜色）进行定性特征编码，对第2、3、4列进行对数函数转换，对第5列进行定量特征二值化处理。
                            使用FeatureUnionExt（自定义的并行处理）类进行部分并行处理的代码如下，
                        #新建将部分特征矩阵进行定性特征编码的对象
                        step2_1 = ('OneHotEncoder', OneHotEncoder(sparse=False))
                        #新建将部分特征矩阵进行对数函数转换的对象
                        step2_2 = ('ToLog', FunctionTransformer(log1p))
                        #新建将部分特征矩阵进行二值化类的对象
                        step2_3 = ('ToBinary', Binarizer())
                        #新建部分并行处理对象
                        #参数transformer_list为需要并行处理的对象列表，该列表为二元组列表，第一元为对象的名称，第二元为对象
                        #参数idx_list为相应的需要读取的特征矩阵的列
                        step2 = ('FeatureUnionExt', FeatureUnionExt(transformer_list=[step2_1, step2_2, step2_3], idx_list=[[0], [1, 2, 3], [4]]))

            2、流水线串行处理：
                pipeline包提供了Pipeline类来进行流水线处理。流水线上除最后一个工作以外，其他都要执行fit_transform方法，且上一个工作输出作为下一个工作的输入。
                    最后一个工作必须实现fit方法，输入为上一个工作的输出；但是不限定一定有transform方法，因为流水线的最后一个工作可能是训练！
                结合并行处理，构建完整的流水线的代码如下，
                    #新建计算缺失值的对象
                    step1 = ('Imputer', Imputer())
                    #新建将部分特征矩阵进行定性特征编码的对象
                    step2_1 = ('OneHotEncoder', OneHotEncoder(sparse=False))
                    #新建将部分特征矩阵进行对数函数转换的对象
                    step2_2 = ('ToLog', FunctionTransformer(log1p))
                    #新建将部分特征矩阵进行二值化类的对象
                    step2_3 = ('ToBinary', Binarizer())
                    #新建部分并行处理对象，返回值为每个并行工作的输出的合并
                    step2 = ('FeatureUnionExt', FeatureUnionExt(transformer_list=[step2_1, step2_2, step2_3], idx_list=[[0], [1, 2, 3], [4]]))
                    #新建无量纲化对象
                    step3 = ('MinMaxScaler', MinMaxScaler())
                    #新建卡方校验选择特征的对象
                    step4 = ('SelectKBest', SelectKBest(chi2, k=3))
                    #新建PCA降维的对象
                    step5 = ('PCA', PCA(n_components=2))
                    #新建逻辑回归的对象，其为待训练的模型作为流水线的最后一步
                    step6 = ('LogisticRegression', LogisticRegression(penalty='l2'))
                    #新建流水线处理对象
                    #参数steps为需要流水线处理的对象列表，该列表为二元组列表，第一元为对象的名称，第二元为对象
                    pipeline = Pipeline(steps=[step1, step2, step3, step4, step5, step6])

        自动化调参：
            #新建网格搜索对象
            #第一参数为待训练的模型
            #param_grid为待调参数组成的网格，字典格式，键为参数名称（格式“对象名称__子对象名称__参数名称”），值为可取的参数值列表
            grid_search = GridSearchCV(pipeline, param_grid={'FeatureUnionExt__ToBinary__threshold':[1.0, 2.0, 3.0, 4.0], 'LogisticRegression__C':[0.1, 0.2, 0.4, 0.8]})
            #训练以及调参
            grid_search.fit(iris.data, iris.target)

        持久化：
            externals.joblib包提供了dump和load方法来持久化和加载内存数据
            #持久化数据
            #第一个参数为内存中的对象
            #第二个参数为保存在文件系统中的名称
            #第三个参数为压缩级别，0为不压缩，3为合适的压缩级别
            dump(grid_search, 'grid_search.dmp', compress=3)

            #加载
            #从文件系统中加载数据到内存中
            grid_search = load('grid_search.dmp')

            注意：组合和持久化都会涉及pickle技术，在sklearn的技术文档中有说明，将lambda定义的函数作为FunctionTransformer的自定义转换函数将不能pickle化

"""

from numpy import log1p
from sklearn.pipeline import Pipeline,FeatureUnion
from sklearn.preprocessing import  FunctionTransformer,Binarizer
from sklearn.model_selection import GridSearchCV
from sklearn.externals.joblib import dump,load


def main():
    pass


if __name__ == '__main__':
    main()

