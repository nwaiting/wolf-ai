#coding=utf-8

"""
    leecode刷题（12）
        输入: 123
        输出: 321
"""

def number_reverse(x):
    new_value = 0
    flag = 1
    if x < 0:
        flag = -1
        x = -x
    while x:
        tmp = x%10
        new_value = new_value * 10 + tmp
        x = int(x/10)
    return new_value*flag

if __name__ == '__main__':
    print(number_reverse(135))
    print(number_reverse(-2457))
