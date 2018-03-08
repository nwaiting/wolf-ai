#coding=utf-8

def common_lcs(s1, s2):
    ls1 = len(s1)
    ls2 = len(s2)
    if ls1 <= 0 or ls2 <= 0:
        return 0,None

    arr = [[0 for clo in xrange(ls2+1)] for row in xrange(ls1+1)]
    re_list = [[0 for clo in xrange(ls2+1)] for row in xrange(ls1+1)]
    for i in xrange(1,ls1+1):
        for j in xrange(1,ls2+1):
            if s1[i-1] == s2[j-1]:
                arr[i][j] = arr[i-1][j-1] + 1
                re_list[i][j] = 1 #斜线
            elif arr[i-1][j] >= arr[i][j-1]:
                arr[i][j] = arr[i-1][j]
                re_list[i][j] = 2 #向上
            else:
                arr[i][j] = arr[i][j-1]
                re_list[i][j] = 3 #向左
    return arr[ls1][ls2],re_list


def print_lcs(l, i_index, j_index):
    if i_index <= 0 or j_index <= 0:
        return
    if l[i_index][j_index] == 1:
        print_lcs(l, i_index-1, j_index-1)
        print s1[i_index-1]
    elif l[i_index][j_index] == 2:
        print_lcs(l, i_index-1, j_index)
    else:
        print_lcs(l, i_index, j_index-1)

if __name__ == '__main__':
    str1 = 'abcbdab'
    str2 = 'bdcaba'
    (nums,res) = common_lcs(str1, str2)
    print nums
    print_lcs(res, len(str1), len(str2))
    print 'lcs'
    print_lcs(res, len(str1), len(str2)-1)
    print 'lcs'
    print_lcs(res, len(str1)-1, len(str2))
