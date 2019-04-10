#coding=utf-8


"""
    分类数据类型在以下情况下非常有用：
        一个字符串变量，只包含几个不同的值。将这样的字符串变量转换为分类变量将会节省一些内存。
        变量的词汇顺序与逻辑顺序("one"，"two"，"three")不同。 通过转换为分类并指定类别上的顺序，排序和最小/最大将使用逻辑顺序，而不是词法顺序。
        作为其他python库的一个信号，这个列应该被当作一个分类变量(例如，使用合适的统计方法或plot类型)。

    常用函数：
        pd.Categorical  使用标准Pandas分类构造函数，我们可以创建一个类别对象
        .describe()     使用分类数据上的.describe()命令，可以得到与类型字符串的Series或DataFrame类似的输出
        obj.cat.categories  获取类别的属性
        obj.ordered         命令用于获取对象的顺序
        series.cat.categories           重命名类别
        Categorical.add.categories()    附加新类别
        Categorical.remove_categories()     删除类别

    分类数据的比较：
        在三种情况下可以将分类数据与其他对象进行比较-
            将等号(==和!=)与类别数据相同长度的类似列表的对象(列表，系列，数组…)进行比较。
            当ordered==True和类别是相同时，所有比较(==，!=，>，>=，<，和<=)分类数据到另一个分类系列。
            将分类数据与标量进行比较。
"""

import numpy as np
import pandas as pd



def main():
    s = pd.Series(['a','b','c','a'], dtype='category')
    print(s)
    print('='*64)

    pc = pd.Categorical(['a','b','c','a','b','c'],['c','b','a','d'])
    print(pc)
    print('='*64)

    # 排序
    pc = pd.Categorical(['a','b','c','a','b','c'],['c','b','a','d'], ordered=True)
    print(pc)
    print('='*64)


    # 描述
    cat = pd.Categorical(["a", "c", "c", np.nan], categories=["b", "a", "c"])
    df = pd.DataFrame({"cat":cat, "s":["a", "c", "c", np.nan]})
    print(df)
    print (df.describe())
    print('='*64)
    print('='*64)

    # 获取类别的属性
    s = pd.Categorical(["a", "c", "c", np.nan], categories=["b", "a", "c"])
    print(s.categories)

    # 获取对象的顺序
    print(s.ordered)
    print('='*64)


    # 重命名类别
    # 重命名类别是通过将新值分配给series.cat.categories属性来完成的
    s = pd.Series(["a","b","c","a"], dtype="category")
    print(s)
    s.cat.categories = ["Group %s" % g for g in s.cat.categories]
    print(s.cat.categories)
    print(s)
    print('='*64)

    # 附加新类别 Categorical.add.categories()
    s = s.cat.add_categories([4])
    print(s.cat.categories)
    print('='*64)

    # 删除类别 Categorical.remove_categories()
    print(s.cat.remove_categories('Group a'))
    print('='*64)
    print('='*64)

    # 分类数据的比较
    cat1 = pd.Series([1,2,3]).astype("category", categories=[1,2,3], ordered=True)
    cat2 = pd.Series([2,2,2]).astype("category", categories=[1,2,3], ordered=True)
    print(cat1>cat2)


























if __name__ == '__main__':
    main()
