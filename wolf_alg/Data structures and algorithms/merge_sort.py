"""
sort alg
"""


def merge(left_list, right_list):
    result = list()
    l, r = 0, 0
    while l < len(left_list) and r < len(right_list):
        if left_list[l] <= right_list[r]:
            result.append(left_list[l])
            l += 1
        else:
            result.append(right_list[r])
            r += 1
    if l < len(left_list):
        result += left_list[l:]
    if r < len(right_list):
        result += right_list[r:]
    return result


def mergesort(data_to_sort):
    if len(data_to_sort) <= 1:
        return data_to_sort

    middle = len(data_to_sort)/2
    left = mergesort(data_to_sort[:middle])
    right = mergesort(data_to_sort[middle:])
    return merge(left, right)


if __name__ == "__main__":
    data_list = [283294, 100, 30, 2342, 34, 23948, 3242, 453, 5675, 5675]
    print mergesort(data_list)

