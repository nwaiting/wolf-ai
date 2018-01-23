# coding: utf-8


def bubble_sort(number_list):
    for i in xrange(len(number_list)):
        for j in xrange(1, len(number_list) - i):
            if number_list[j-1] > number_list[j]:
                number_list[j-1], number_list[j] = number_list[j], number_list[j-1]


def select_sort(number_list):
    for i in xrange(len(number_list)):
        tmp = i
        for j in xrange(i+1, len(number_list)):
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
    numbers = [100, 5, 2000, 260, 189, 368, 555, 999, 1649, 2597]
    #bubble_sort(numbers)
    #select_sort(numbers)
    insertion_sort(numbers)
    print numbers
