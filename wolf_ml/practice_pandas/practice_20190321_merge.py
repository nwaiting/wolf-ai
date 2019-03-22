#coding=utf-8


"""
    Pandas具有功能全面的高性能内存中连接操作，与SQL等关系数据库非常相似。Pandas提供了一个单独的merge()函数，作为DataFrame对象之间所有标准数据库连接操作的入口
        pd.merge(left, right, how='inner', on=None, left_on=None, right_on=None,left_index=False, right_index=False, sort=True)
        left - 一个DataFrame对象。
        right - 另一个DataFrame对象。
        on - 列(名称)连接，必须在左和右DataFrame对象中存在(找到)。
        left_on - 左侧DataFrame中的列用作键，可以是列名或长度等于DataFrame长度的数组。
        right_on - 来自右的DataFrame的列作为键，可以是列名或长度等于DataFrame长度的数组。
        left_index - 如果为True，则使用左侧DataFrame中的索引(行标签)作为其连接键。 在具有MultiIndex(分层)的DataFrame的情况下，级别的数量必须与来自右DataFrame的连接键的数量相匹配。
        right_index - 与右DataFrame的left_index具有相同的用法。
        how - 它是left, right, outer以及inner之中的一个，默认为内inner。 下面将介绍每种方法的用法。
            如何合并参数指定如何确定哪些键将被包含在结果表中。如果组合键没有出现在左侧或右侧表中，则连接表中的值将为NA
                left
                    LEFT OUTER JOIN 使用左侧对象的键
                right
                    RIGHT OUTER JOIN    使用右侧对象的键
                outer
                    FULL OUTER JOIN 使用键的联合
                inner
                    INNER JOIN  使用键的交集
                与sql等效的参数
        sort - 按照字典顺序通过连接键对结果DataFrame进行排序。默认为True，设置为False时，在很多情况下大大提高性能。
"""


import numpy as np
import pandas as pd



def main():
    left = pd.DataFrame({'id':[1,2,3,4,5],
            'Name': ['Alex', 'Amy', 'Allen', 'Alice', 'Ayoung'],
            'subject_id':['sub1','sub2','sub4','sub6','sub6']}
            )
    right = pd.DataFrame({'id':[1,2,3,4,5,5],
            'Name': ['Billy', 'Brian', 'Bran', 'Bryce', 'Betty','Bettydouble'],
            'subject_id':['sub2','sub4','sub3','sub6','sub5','subdouble']}
            )
    print(left)
    print("="*64)
    print(right)
    print("="*64)

    # 根据标签合并
    print(pd.merge(left, right, on=['id']))
    print("="*64)

    # 合并多个标签，即两个标签值对应，不对应的丢掉
    print(pd.merge(left, right, on=['id','subject_id']))
    print("="*64)

    # 合并使用how
    print(pd.merge(left, right, on=['subject_id']))
    print(pd.merge(left, right, on=['subject_id'], how='left'))
    print(pd.merge(left, right, on=['subject_id'], how='left').subject_id.shift(1).values)
    first = pd.merge(left, right, on=['subject_id'], how='left').id_x.values
    second = pd.merge(left, right, on=['subject_id'], how='left').id_x.shift(1).values
    ac_pairs = list(zip(first, second))
    print("ac_pairs=",ac_pairs)
    ac_pairs.pop(0)
    print("ac_pairs=",ac_pairs)
    print(list(map(lambda s: str(int(s[0])) + '_' + str(int(s[1])), ac_pairs)))
    print("="*64)
    return
    print(pd.merge(left, right, on=['subject_id'], how='right'))
    print(pd.merge(left, right, on=['subject_id'], how='inner'))
    print(pd.merge(left, right, on=['subject_id'], how='outer'))




























if __name__ == '__main__':
    main()
