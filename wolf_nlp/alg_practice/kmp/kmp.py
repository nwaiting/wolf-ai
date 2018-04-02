#coding=utf8

"""
    暴力匹配字符串
"""
def violentMatch(s, p):
    i = len(s)
    j = len(p)
    i_t = 0
    j_t = 0
    cmp_times = 0
    while i_t < i and j_t < j:
        cmp_times += 1
        if debug_log:
            print('violent compare times {0} {1}'.format(i_t, j_t))
        if s[i_t] == p[j_t]:
            i_t += 1
            j_t += 1
        else:
            i_t = i_t - j_t + 1
            j_t = 0
    if debug_log:
        print('violent compare times ', cmp_times)
    if j_t == j:
        return i_t - j_t
    else:
        return -1

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
    cmp_times = 0
    while s_i < s_len and p_j <  p_len:
        cmp_times += 1
        if debug_log:
            print('kmp compare times {0} {1}'.format(s_i, p_j))
        if -1 == p_j or s[s_i] == p[p_j]:
            s_i += 1
            p_j += 1
        else:
            p_j = next_arr[p_j]
    if debug_log:
        print('kmp compare times ', cmp_times)
    if p_j == p_len:
        return s_i - p_j
    else:
        return -1

"""
    测试发现kmp竟然比暴力搜索比较的次数多，说明原因？
    在有些测试条件下，kmp比较次数比violent次数多
"""
if __name__ == '__main__':
    pt = 'abab'
    so = 'abacabadabaeabafabab'
    debug_log = True
    import time
    begin = time.time()
    cmp_times = 20000
    if not debug_log:
        for _ in range(cmp_times):
            kmpsearch(so, pt)
    print('kmp cost time ', time.time() - begin)
    print(kmpsearch(so, pt))

    begin = time.time()
    if not debug_log:
        for _ in range(cmp_times):
            violentMatch(so, pt)
    print('violent cost time ', time.time() - begin)
    print(violentMatch(so, pt))

    #print(getNextArray(first_str))
