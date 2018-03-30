#coding=utf8

"""
    getNextArray(s)：获取一个最大公共前缀的数组
    kmp中next数组查找一个字符串中最大除当前字符外的最长相同前缀后缀
"""
def getNextArray(s):
    next_array = []
    if len(s) <= 1:
        return [0]

    next_array = [0 for _ in range(len(s))]
    next_array[0] = -1
    k = -1
    j = 0
    while j < len(s) - 1:
        if -1 == k or s[k] == s[j]:
            k += 1
            j += 1
            # 如果相等后 在数组下一个才会有显示
            # next_array[j] = k
            # 优化：参考 http://wiki.jikexueyuan.com/project/kmp-algorithm/define.html
            if s[k] != s[j]:
                next_array[j] = k
            else:
                next_array[j] = next_array[k]
        else:
            k = next_array[k]
    return next_array

def kmpsearch(s, p):
    if len(s) <= 0 or len(p) <= 0:
        return -1
    s_len = len(s)
    p_len = len(p)
    s_i = 0
    p_j = 0
    next_arr = getNextArray(p)
    while s_i < s_len and p_j <  p_len:
        if -1 == p_j or s[s_i] == p[p_j]:
            s_i += 1
            p_j += 1
        else:
            p_j = next_arr[p_j]

    if p_j == p_len:
        return s_i - p_j
    else:
        return -1

if __name__ == '__main__':
    pt = 'abab'
    so = 'abcdslfjlsadfaababsadfasdfasf'
    print(kmpsearch(so, pt))

    #print(getNextArray(first_str))
