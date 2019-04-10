#coding=utf-8



"""
    sklearn超参数优化方法：
        sklearn 提供了两种通用的参数优化方法：网络搜索和随机采样：
            1、网格搜索交叉验证（GridSearchCV）：以穷举的方式遍历所有可能的参数组合
            2、随机采样交叉验证（RandomizedSearchCV）：依据某种分布对参数空间采样，随机的得到一些候选参数组合方案
                RandomizedSearchCV类实现了在参数空间上进行随机搜索的机制，其中参数的取值是从某种概率分布中抽取的，这个概率分布描述了对应的参数的所有取值情况的可能性，
                这种随机采样机制与网格穷举搜索相比，有两大优点：
                    a、相比于整体参数空间，可以选择相对较少的参数组合数量
                    b、添加参数节点不影响性能，不会降低效率

    超参数空间的搜索技巧：
        1、指定一个合适的目标测度对模型进行估计
            默认情况下，参数搜索使用estimator的score函数来评估模型在某种参数配置下的性能：
                分类器对应于 sklearn.metrics.accuracy_score
                回归器对应于sklearn.metrics.r2_score
            但是在某些应用中，其他的评分函数获取更加的合适。（比如在非平衡的分类问题中，准确率sccuracy_score通常不管用。这时，可以通过参数scoring来指定GridSearchCV类或者RandomizedSearchCV类内部用我们自定义的评分函数）
        2、使用SKlearn的PipeLine将estimators和他们的参数空间组合起来
        3、合理划分数据集：开发集（用于GridSearchCV）+测试集（Test）使用model_selection.train_test_split()函数来搞定！
        4、并行化：（GridSearchCV）和（RandomizedSearchCV）在参数节点的计算上可以做到并行计算，这个通过参数”n_jobs“来指定
        5、提高在某些参数节点上发生错误时的鲁棒性：在出错节点上只是提示警告。可以通过设置参数error_score=0(or=np.NaN)来搞定

"""

from sklearn.model_selection import GridSearchCV,RandomizedSearchCV,ParameterGrid,ParameterSampler,fit_grid_point


def main():
    pass












if __name__ == '__main__':
    main()
