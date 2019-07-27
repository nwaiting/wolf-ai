# coding: utf-8

"""
    对5,3,8,6,4这个无序序列进行冒泡排序。
        首先从后向前冒泡，4和6比较，把4交换到前面，序列变成5,3,8,4,6。
        同理4和8交换，变成5,3,4,8,6,3和4无需交换。
        5和3交换，变成3,5,4,8,6,3.
        这样一次冒泡就完了，把最小的数3排到最前面了。对剩下的序列依次冒泡就会得到一个有序序列。冒泡排序的时间复杂度为O(n^2)
"""

def bubble_sort(number_list):
    for i in xrange(len(number_list)):
        for j in xrange(1, len(number_list) - i):
            if number_list[j-1] > number_list[j]:
                number_list[j-1], number_list[j] = number_list[j], number_list[j-1]


def select_sort(number_list):
    for i in range(len(number_list)):
        tmp = i
        for j in range(i+1, len(number_list)):
            if number_list[j] < number_list[tmp]:
                tmp = j
        if tmp != i:
            number_list[i], number_list[tmp] = number_list[tmp], number_list[i]


def insertion_sort(number_list):
    for i in xrange(1, len(number_list)):
        tmp = i
        tmp_value = number_list[i]
        for j in xrange(i-1, -1, -1):
            if number_list[j] > tmp_value:
                number_list[j+1] = number_list[j]
                tmp = j
            else:
                break
        number_list[tmp] = tmp_value


if __name__ == "__main__":
    numbers = [300, 5, 2000, 260, 189, 368, 555, 999, 1649, 2597]
    bubble_sort(numbers)
    #select_sort(numbers)
    #insertion_sort(numbers)
    print(numbers)
