#coding=utf-8

"""
编辑距离：
把图中上面的源串S[0…i] = “ALGORITHM”编辑成下面的目标串T[0…j] = “ALTRUISTIC”，
我们枚举字符串S和T最后一个字符s[i]、t[j]对应四种情况：（字符-空白）（空白-字符）(字符-字符)（空白-空白）
由于其中的（空白-空白）是多余的编辑操作。所以，事实上只存在以下3种情况：
1、下面的目标串空白，即S + 字符X，T + 空白，S变成T，意味着源串要删字符
    dp[i - 1, j] + 1
2、上面的源串空白，S + 空白，T + 字符，S变成T，最后，在S的最后插入“字符”，意味着源串要添加字符
    dp[i, j - 1] + 1
3、上面源串中的的字符跟下面目标串中的字符不一样，即S + 字符X，T + 字符Y，S变成T，意味着源串要修改字符
    dp [i - 1, j - 1] + (s[i] == t[j] ? 0 : 1)

dp[i,j]表示表示源串S[0…i] 和目标串T[0…j] 的最短编辑距离
dp[i, j] = min { dp[i - 1, j] + 1,  dp[i, j - 1] + 1,  dp[i - 1, j - 1] + (s[i] == t[j] ? 0 : 1) }
分别表示：删除1个，添加1个，替换1个（相同就不用替换）

应用
　　DNA分析
　　拼字检查
　　语音辨识
　　抄袭侦测
"""

def edit_distance(s1, s2):
    ls1 = len(s1)
    ls2 = len(s2)
    if ls1 <= 0 or ls2 <= 0:
        return max(ls1, ls2)

    arr = [[0 for clo in xrange(ls2+1)] for row in xrange(ls1+1)]
    for i in xrange(ls1+1):
        arr[i][0] = i
    for j in xrange(ls2+1):
        arr[0][j] = j
    for i in xrange(1,ls1+1):
        for j in xrange(1,ls2+1):
            if s1[i-1] == s2[j-1]:
                arr[i][j] = arr[i-1][j-1]
            else:
                arr[i][j] = min(arr[i-1][j-1]+1, arr[i-1][j]+1,arr[i][j-1]+1)
    return arr[i][j]


if __name__ == '__main__':
    s1 = 'hello'
    s2 = 'halloe'
    ell = edit_distance(s1, s2)
    print ell
    print '相似性为 {0}'.format(1-float(ell)/max(len(s1),len(s2)))
