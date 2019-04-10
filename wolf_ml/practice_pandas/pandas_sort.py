#coding=utf-8



"""
    有两种排序方法：
        1、按标签
        2、按实际值
            sort_values()提供了从mergeesort，heapsort和quicksort中选择算法的一个配置。Mergesort是唯一稳定的算法
    参考：https://www.yiibai.com/pandas/python_pandas_working_with_text_data.html
"""

import numpy as np
import pandas as pd


def main():
    df = pd.DataFrame(np.random.randn(10,4),index=[1,4,6,2,3,5,9,8,0,7],columns=['col1','col2','col3','col4'])
    print(df)
    print("=="*32)

    # sort_index() 行、列标签排序
    # 使用sort_index()方法，通过传递axis参数和排序顺序，可以对DataFrame进行排序。 默认情况下，按照升序对行标签进行排序
    print(df.sort_index(ascending=False))
    print(df.sort_index(ascending=False, axis=1))
    print("=="*32)

    # sort_values 实际值排序
    print(df.sort_values(by='col1', ascending=True))
    print(df.sort_values(by=0, ascending=False, axis=1))
    print(df.sort_values(by=['col1','col2'], kind='mergesort'))





if __name__ == '__main__':
    main()
