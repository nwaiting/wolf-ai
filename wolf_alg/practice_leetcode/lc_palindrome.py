#coding=utf-8

"""
    https://blog.csdn.net/qwerty200696/article/details/79053770
"""

# 1、就是看翻转后的数值和原始数值是否一致
# 2、就是看翻转一半的数值是否和原来数值一样
def palindrome_int(n):
    left = 0
    while n > left:
        left = left*10 + n%10
        n = int(n/10)
    #print("left={},right={}".format(left, n))
    return n==left or n==int(left/10)


def palindrome_str(s):
    length = len(s)
    mid = int(length/2)
    if length%2==0:
        #print("left={},right={}".format(s[:mid],s[:mid-1:-1]))
        return s[:mid] == s[:mid-1:-1]
    else:
        return s[:mid] == s[:mid:-1]





if __name__ == '__main__':
    print(palindrome_int(121))
    print(palindrome_int(1212))
    print(palindrome_int(1221))
    print(palindrome_int(12221))
    print(palindrome_str("12221"))
    print(palindrome_str("1221"))
    print(palindrome_str("1212"))
