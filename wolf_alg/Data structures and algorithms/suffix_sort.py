#coding=utf-8

class strItem(object):
    def __init__(self, s=None, index=None, pre=None):
        self.s = s
        self.index = index
        self.pre = pre

def Print(l):
    for i in l:
        print "{0},{1},{2}".format(i.index, i.s, i.pre)

def itemCmp(item1, item2):
    i = 0
    while i < len(item1.s) and i < len(item2.s):
        if item1.s[i] < item2.s[i]:
            return 1
        elif item1.s[i] > item2.s[i]:
            return -1
        i += 1

    if len(item1.s) < len(item2.s):
        return 1
    elif len(item1.s) > len(item2.s):
        return -1
    else:
        return 0

def common_pre(s1, s2):
    i = 0
    while i < len(s1) and i < len(s2):
        if s1[i] == s2[i]:
            i += 1
        else:
            return i
    return i

def suffix_sort(s):
    str_lists = list()
    for i in xrange(len(s)):
        str_lists.append(strItem(s[i:], i+1, 0))

    b = sorted(str_lists, key=lambda x :x.s)
    #Print(b)
    """
    或者下面方法排序
    print "==================="
    b = sorted(str_lists, cmp=itemCmp)
    Print(b)
    """
    for i in xrange(1, len(b)):
        b[i].pre = common_pre(b[i-1].s, b[i].s)

if __name__ == '__main__':
    string = 'ababdhkab'
    suffix_sort(string)
