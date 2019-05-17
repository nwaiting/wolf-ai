#coding=utf-8


"""
    reverse string
        abcd
        dcba
"""
def reverseString(s):
    length = len(s)
    s = list(s)
    for i in range(int(len(s)/2)):
        s[i],s[length-i-1]=s[length-i-1],s[i]
    return s


"""
    reverse word
        hello word
        word hello
"""
def reverse_word(s):
    res = [0]*len(s)
    s = list(s)
    pre_index = len(s)-1
    j = 0
    for i in range(len(s)-1,-1,-1):
        if s[i] == ' ':
            for k in range(i+1,pre_index+1):
                res[j] = s[k]
                j += 1
            pre_index = i-1
        if i == 0:
            for k in range(i,pre_index+1):
                res[j] = s[k]
                j += 1
    return res


if __name__ == '__main__':
    print(reverseString("abcd"))
    print(reverse_word("hello this word"))
