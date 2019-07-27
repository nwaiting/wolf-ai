#coding=utf-8


"""
    冒泡排序是通过相邻的比较和交换。而选择排序是通过对整体的选择。
    举个栗子，对5,3,8,6,4这个无序序列进行简单选择排序，首先要选择5以外的最小数来和5交换，也就是选择3和5交换，一次排序后就变成了3,5,8,6,4.对剩下的序列一次进行选择和交换，最终就会得到一个有序序列。
        其实选择排序可以看成冒泡排序的优化，因为其目的相同，只是选择排序只有在确定了最小数的前提下才进行交换，大大减少了交换的次数。

    一趟遍历完记录最小的数，放到第一个位置；在一趟遍历记录剩余列表中的最小的数，继续放置 ！！！！

"""

def select_sort(l):
    for i in xrange(len(l)-1):
        min_index = i
        for j in xrange(i+1, len(l)):
            if l[j] < l[min_index]:
                min_index = j
        if min_index != i:
            l[min_index],l[i] = l[i],l[min_index]
    return l

if __name__ == '__main__':
    data = [1,21,13,5,10,20,2,3,5]
    print select_sort(data)
