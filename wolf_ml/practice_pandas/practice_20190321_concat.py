#coding=utf-8


"""
    Pandas提供了各种工具(功能)，可以轻松地将Series，DataFrame和Panel对象组合在一起
        pd.concat(objs,axis=0,join='outer',join_axes=None,ignore_index=False)
            objs - 这是Series，DataFrame或Panel对象的序列或映射。
            axis - {0，1，...}，默认为0，这是连接的轴。
            join - {'inner', 'outer'}，默认inner。如何处理其他轴上的索引。联合的外部和交叉的内部。
            ignore_index − 布尔值，默认为False。如果指定为True，则不要使用连接轴上的索引值。结果轴将被标记为：0，...，n-1。
            join_axes - 这是Index对象的列表。用于其他(n-1)轴的特定索引，而不是执行内部/外部集逻辑。

        常见两种连接：
            连接对象
            附加连接

    Pandas为时间序列数据的工作时间提供了一个强大的工具，尤其是在金融领域。在处理时间序列数据时，我们经常遇到以下情况 -
        生成时间序列
        将时间序列转换为不同的频率
"""

import numpy as np
import pandas as pd


def main():
    one = pd.DataFrame({
            'Name': ['Alex', 'Amy', 'Allen', 'Alice', 'Ayoung'],
            'subject_id':['sub1','sub2','sub4','sub6','sub5'],
            'Marks_scored':[98,90,87,69,78]},
            index=[1,2,3,4,5]
            )
    two = pd.DataFrame({
            'Name': ['Billy', 'Brian', 'Bran', 'Alice', 'Betty'],
            'subject_id':['sub2','sub4','sub3','sub6','sub5'],
            'Marks_scored':[89,80,79,97,88]},
            index=[1,2,3,4,5]
            )

    print(one)
    print("="*64)
    print(two)
    print("="*64)
    print(pd.concat([one,two]))
    print("="*64)

    df_tmp = pd.concat([one,two])
    print(df_tmp[df_tmp.Name=="Alice"])
    print("+"*64)

    print(pd.concat([one,two], keys=['x','y']))
    print("="*64)

    #重建索引
    print(pd.concat([one,two], keys=['x','y'], ignore_index=True))
    print("="*64)

    # 如果需要沿axis=1添加两个对象，则会添加新列
    print(pd.concat([one,two], axis=1))
    print("="*64)

    # append 使用附加连接
    print(one.append([two, one], ignore_index=True))
    print("="*64)

    # 时间序列
    print(pd.datetime.now())
    print(pd.Timestamp('2019-03-21'))
    print(pd.Timestamp(1588686880,unit='s'))
    print("="*64)

    #创建一个时间范围
    pd_time = pd.date_range("12:00","23:59",freq='30min').time
    print(pd_time)
    print("="*64)
    #改变频率
    print(pd.date_range("12:00","23:59",freq='H').time)
    print("="*64)
    #转换为时间戳
    s = pd.Series(['2009/11/23', '2019.12.31', None])
    pd_time = pd.to_datetime(s)
    print(pd_time.values)










if __name__ == '__main__':
    main()
