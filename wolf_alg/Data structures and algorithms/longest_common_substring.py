#coding=utf-8

"""
暴力搜索
"""
def common_max_length(s1, s2):
    min_l = min(len(s1), len(s2))
    max_l = 0
    for i in xrange(min_l):
        if s1[i] == s2[i]:
            max_l += 1
        else:
            break
    return max_l

def common_substring_base(s1, s2):
    max_len = 0
    for i in xrange(len(s1)):
        for j in xrange(len(s2)):
            tmp_max = common_max_length(s1[i:], s2[j:])
            if tmp_max > max_len:
                max_len = tmp_max
    return max_len

"""
dp 算法
"""
def common_substring_dp(s1, s2):
    ls1 = len(s1)
    ls2 = len(s2)
    dis = [[0 for i in xrange(ls2)] for j in xrange(ls1)]
    #print dis
    max_len = 0
    for i in xrange(ls1):
        for j in xrange(ls2):
            if s1[i] == s2[j]:
                if i > 0 and j > 0:
                    #print i,j
                    dis[i][j] = dis[i-1][j-1] + 1
                else:
                    dis[i][j] = 1

                if dis[i][j] > max_len:
                    max_len = dis[i][j]
    return max_len

"""
后缀数组
"""
def get_common_pre(s1, s2):
    i = 0
    count = 0
    count_flag = 0
    while i < len(s1) and i < len(s2):
        if s1[i] != '@' and s2[i] != '@' and s1[i] == s2[i]:
            count += 1
        else:
            break
        i += 1

    j = i
    while j < len(s1):
        if s1[j] == '@':
            count_flag |= 0x01
        j += 1

    while i < len(s2):
        if s2[i] == '@':
            count_flag |= 0x02
        i += 1

    if count_flag == 0 or count_flag == 0x03:
        return 0
    return count

def common_substring_suffix(s1, s2):
    s = s1 + '@' + s2
    l = list()
    for i in xrange(len(s)+1):
        l.append(s[i:])
    l.sort()

    max_len = 0
    for i in xrange(1, len(l)):
        pre_max =get_common_pre(l[i-1], l[i])
        if pre_max > max_len:
            max_len = pre_max
    return max_len

if __name__ == '__main__':
    str1 = 'sdlfhaslkdhfklaslsdhflhasdfkhashdfklhsadklhflasdfhdklghasdkhfklhasdfklhasdkhfklsdhflabcdefghijkdklfhlasdhsdf;aslgjlkashdglkashdkghalsdhgfklasdhkf'
    str2 = 'sdlfjasldhfkasdhgfsdflkashdflhasdkhfklsahdfklhasdfkhklashdfklasdfkhkasdhfkasdfabcdefghijklmnsfdas;dfjasdgkjaslsldhfklashdfklhsdflkhdshlhkl'
    from time import time
    first_t = time()
    print common_substring_base(str1, str2)
    second_t = time()
    print 'base cost ', second_t - first_t
    print common_substring_dp(str1, str2)
    third_t = time()
    print 'dp cost ', third_t - second_t
    print common_substring_suffix(str1, str2)
    print 'suf cost ', time() - third_t
