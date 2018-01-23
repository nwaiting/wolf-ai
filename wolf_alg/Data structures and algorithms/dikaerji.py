#coding=utf-8

#非递归实现笛卡尔积
def both_list(l_one, l_two):
    if len(l_one) <= 0 or len(l_two) <= 0:
        return l_one if len(l_one) > 0 else l_two

    result_list = list()
    for i in xrange(0, len(l_one)):
        for j in xrange(0, len(l_two)):
            if isinstance(l_one[i], list):
                t = l_one[i][:]
                t.append(l_two[j])
                result_list.append(t)
            else:
                result_list.append([l_one[i], l_two[j]])
    return result_list


def get_dis(l):
    if len(l) <= 1:
        return l

    tmp_list1 = l[0]
    for i in xrange(1, len(l)):
        tmp_list1 = both_list(tmp_list1, l[i])
    return tmp_list1

#递归实现笛卡尔积
def dkrj_recursion(total_list, result_list, list_index, current_list):
    if list_index < len(total_list) - 1:
        for item in total_list[list_index]:
            tmp = current_list[:]
            tmp.append(item)
            dkrj_recursion(total_list, result_list, list_index+1, tmp)
    elif list_index == len(total_list) - 1:
        for item in total_list[list_index]:
            tmp = current_list[:]
            tmp.append(item)
            result_list.append(tmp)
    return result_list

if __name__ == '__main__':
    do_list = [[1,2,3],[4,5,6],[7,8,9]]
    res = list()
    flag = 0
    if flag == 0:
        res = get_dis(do_list)
    else:
        dkrj_recursion(do_list, res, 0, list())
    for i in xrange(0, len(res)):
        print res[i]
