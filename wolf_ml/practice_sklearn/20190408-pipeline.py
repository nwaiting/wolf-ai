# coding=utf-8


from sklearn.pipeline import Pipeline,make_pipeline


"""
    Pipeline:
        Pipeline可以将许多算法模型串联起来，比如将特征提取、归一化、分类组织在一起形成一个典型的机器学习问题工作流。
        主要带来两点好处：
            1、直接调用fit和predict方法来对pipeline中的所有算法模型进行训练和预测
            2、可以结合grid search对参数进行选择。

        使用介绍：
            通过steps参数，设定数据处理流程。格式为('key','value')，key是自己为这一step设定的名称，value是对应的处理类。最后通过list将这些step传入。
            前n-1个step中的类都必须有transform函数，最后一步可有可无，一般最后一步为模型
            iris=load_iris()
            pipe=Pipeline(steps=[('pca',PCA()),('svc',SVC())])
            pipe.fit(iris.data,iris.target)
            训练得到的是一个模型，可直接用来预测，预测时，数据会从step1开始进行转换，避免了模型用来预测的数据还要额外写代码实现。
            pipe.predict(iris.data)

            在pipeline中estimator的参数通过使用<estimator>__<parameter>语法来获取
            pipe.set_params(svc__C=10)

    make_pipeline:
        通过make_pipeline函数实现：它是Pipeline类的简单实现，只需传入每个step的类实例即可，不需自己命名，自动将类的小写设为该step的名，
        同时可以通过set_params重新设置每个类里边需传入的参数，设置方法为step的name__parma名=参数值:
            p=make_pipeline(RobustScaler(), Lasso(alpha =0.0005, random_state=1))
            p.set_params(lasso__alpha=0.0001) #将alpha从0.0005变成0.0001

"""


from sklearn.datasets import load_iris
from sklearn.pipeline import make_pipeline, Pipeline, FeatureUnion, make_union
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV


def f1():
    iris = load_iris()
    pipe = Pipeline(steps=[('svc', SVC())])
    print(pipe.named_steps['svc'])
    pipe.set_params(svc__C=10)
    print(pipe.named_steps['svc'])

    # 直接训练
    # pipe.fit(iris.data, iris.target)

    # 网格搜索训练
    params = dict(svc__C=[10,20,30], svc__gamma=[0.01,0.5,0.8])
    grid = GridSearchCV(pipe, param_grid=params)
    grid.fit(iris.data, iris.target)

    print(grid.best_params_)
    print(grid.predict(iris.data))


    # 并行训练
    # pipeline包提供了FeatureUnion类来进行整体并行处理，如下，










if __name__ == '__main__':
    f1()
