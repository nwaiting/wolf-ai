#coding=utf-8


"""
    实际上单个索引的pivot_table 与groupby得到的结果一样，可以这样说，pivot_table是高级版本的groupby，提供了很多groupby不能实现的功能
        多个索引列：
            pd.pivot_table(df,index=['menu','star'])
        特定列的统计
            上面的分析中包含了多列的平均值，假如我们只想看其中的readCnt 列，可以传入values参数
            pd.pivot_table(df,index=['menu','star'],values='readCnt')
        规定特定的聚合函数
            此时，我们也会考虑，这个地方是不是只能是平均值，回答当然是no，还可以通过aggfunc传入其他的参数，以获得不同的结果
            pd.pivot_table(df,index=['menu','star'],values='readCnt',aggfunc=np.sum)
        传入多个聚合函数
            pd.pivot_table(df,index=['menu','star'],values='readCnt',aggfunc=[np.sum,len])
        传入columns参数
            pd.pivot_table(df,index=['menu','star'],values='readCnt',columns='userLevel',aggfunc=[np.sum,len])
        传入fill_value参数，处理缺失值
            上面的例子虽然将index显示完整了，但是仍然有很多缺失值NaN(not a number),显示在这里给人感觉不舒服的话，可以在参数中传入fill_value
            pd.pivot_table(df,index=['userLevel','menu'],values='readCnt',columns='star',aggfunc=[np.sum,len],fill_value=0)

    参考：
        https://www.cnblogs.com/onemorepoint/p/9508910.html?utm_source=debugrun&utm_medium=referral     pandas pivot_table 活学活用实例教程
        http://python.jobbole.com/81212/    详解 Pandas 透视表（pivot_table）
"""

import numpy as np
import pandas as pd

def main():
    pass















if __name__ == '__main__':
    main()
