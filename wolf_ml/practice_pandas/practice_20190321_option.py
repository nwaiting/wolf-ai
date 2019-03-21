#coding=utf-8


"""
    pandas提供自定义其行为的某些方面，大多数用来显示
    常用函数：
        get_option()
        set_option()
        reset_option()
        describe_option()
        option_context()

    常用参数：
        display.max_rows 要显示的最大行数
        display.max_columns 要显示的最大列数
        display.expand_frame_repr 显示数据帧以拉伸页面
        display.max_colwidth 显示最大列宽
        display.precision 显示十进制数的精度

"""


import numpy as np
import pandas as pd


def main():
    # get_option(param)需要一个参数，并返回下面输出中给出的值
    # display.max_rows 显示默认值。解释器读取此值并显示此值作为显示上限的行
    print(pd.get_option("display.max_rows"))
    print("=="*32)

    print(pd.get_option("display.max_columns"))
    print("=="*32)

    # set_option 设置参数值
    pd.set_option("display.max_columns", 80)
    print(pd.get_option("display.max_columns"))
    print("=="*32)


    # reset_option接受一个参数，并将该值设置为默认值
    pd.reset_option("display.max_columns")
    print(pd.get_option("display.max_columns"))
    print("=="*32)

    #describe_option打印参数的描述
    print(pd.describe_option("display.max_rows"))
    print("=="*32)

    # 使用option_context()，可以临时设置该值
    with pd.option_context("display.max_rows",10):
        print(pd.get_option("display.max_rows"))
        print(pd.get_option("display.max_rows"))
    print("=="*32)


































if __name__ == '__main__':
    main()
