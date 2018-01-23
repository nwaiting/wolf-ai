#coding=utf-8
"""
    descartes alg
    2016-09-01 20:07
"""

"""
    loop
"""

def getDis(list_item, list_item1):
    temp_list = list()
    for iitem in list_item:
        for iitem2 in list_item1:
            temp_l = str()
            temp_l += str(iitem) + "\t"
            temp_l += str(iitem2) + "\t"
            temp_list.append(temp_l)
    return temp_list

def getNDis(total_list):
    list_result = total_list[0]
    for i in range(1, len(total_list)):
        list_result = getDis(list_result, total_list[i])
    print "loop result leng {0}".format(len(list_result))
    for ii in list_result:
        print "{0}\n".format(ii)


"""
    recursion
"""

def recursion(double_list, result_list, layer, current_list):
    if layer < len(double_list) - 1:
        if len(double_list[layer]) == 0:
            recursion(double_list, result_list, layer + 1, current_list)
        else:
            """
                不断递归
            """
            for iitem in double_list[layer]:
                new_list = current_list[0:]
                new_list.append(iitem)
                recursion(double_list, result_list, layer + 1, new_list)
    elif layer == len(double_list) - 1:
        if len(double_list[layer]) == 0:
            result_list.append(current_list)
        else:
            """
                最后退出的条件
            """
            for iitem in double_list[layer]:
                new_list = current_list[0:]
                new_list.append(iitem)
                result_list.append(new_list)


def main():
    tot_items = list()

    tot_item = list()
    tot_item = ["king","of","the","world"]
    tot_items.append(tot_item)

    tot_item = list()
    tot_item = ["cs", "app"]
    tot_items.append(tot_item)

    tot_item = list()
    tot_item = ["good", "cool", "dev"]
    tot_items.append(tot_item)

    tot_item = list()
    tot_item = ["king", "of", "the"]
    tot_items.append(tot_item)

    getNDis(tot_items)

    result_list = list()
    temp_list = list()
    recursion(tot_items, result_list, 0, temp_list)
    print "recursion result leng {0}".format(len(result_list))
    for i in result_list:
        print "{0}".format(i)
    return

if __name__ == '__main__':
    main()
