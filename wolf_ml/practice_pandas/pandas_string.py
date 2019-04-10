#coding=utf-8


"""
    字符串常用函数：
        lower() 将Series/Index中的字符串转换为小写。
        upper() 将Series/Index中的字符串转换为大写。
        len() 计算字符串长度。
        strip() 帮助从两侧的系列/索引中的每个字符串中删除空格(包括换行符)。
        split(' ') 用给定的模式拆分每个字符串。
        cat(sep=' ') 使用给定的分隔符连接系列/索引元素。
        get_dummies() 返回具有单热编码值的数据帧(DataFrame)。
        contains(pattern) 如果元素中包含子字符串，则返回每个元素的布尔值True，否则为False。
        replace(a,b) 将值a替换为值b。
        repeat(value) 重复每个元素指定的次数。
        count(pattern) 返回模式中每个元素的出现总数。
        startswith(pattern) 如果系列/索引中的元素以模式开始，则返回true。
        endswith(pattern) 如果系列/索引中的元素以模式结束，则返回true。
        find(pattern) 返回模式第一次出现的位置。
        findall(pattern) 返回模式的所有出现的列表。
        swapcase 变换字母大小写。
        islower() 检查系列/索引中每个字符串中的所有字符是否小写，返回布尔值
        isupper() 检查系列/索引中每个字符串中的所有字符是否大写，返回布尔值
        isnumeric() 检查系列/索引中每个字符串中的所有字符是否为数字，返回布尔值。

"""

import numpy as np
import pandas as pd



def main():

    s = pd.Series(['Tom', 'William Rick', 'John', 'Alber@t', np.nan, '1234','SteveMinsu'])
    print (s.str.lower())
    print (s.str.upper())
    print (s.str.len())
    print (s.str.strip())
    print (s.str.split(' '))
    print (s.str.cat(sep=' <=> '))
    print (s.str.get_dummies())
    print (s.str.contains(' '))
    print (s.str.replace('@','$'))
    print (s.str.repeat(2))
    print (s.str.count('m'))
    print (s.str.startswith('T'))
    print (s.str.endswith('t'))
    print (s.str.find('e'))
    print (s.str.findall('e'))
    print (s.str.swapcase())
    print (s.str.islower())
    print (s.str.isupper())
    print (s.str.isnumeric())

def main2():
    N = 10
    df = pd.DataFrame({
           'A': pd.date_range(start='20190320',periods=N,freq='D'),
           'x': np.linspace(0,stop=N-1,num=N),
           'y': np.random.rand(N),
           'C': np.random.choice(['Low','Medium','High'],N).tolist(),
           'D': np.random.normal(100, 10, size=(N)).tolist(),
           'E': ['Tom', 'William Rick', 'John', 'Alber@t', np.nan, '1234','SteveMinsu','2345',np.nan, np.nan]
        })
    print(df)
    print("=="*32)

    print(df.loc[:,'E'].str.lower())




if __name__ == '__main__':
    main()
    main2()
