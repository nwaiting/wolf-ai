import sys
import os
import math


def main():
    """
        python cal_split.py data 1
    """
    def save_split_data(filename, data, protein_name):
        with open(filename, 'ab') as f:
            f.write((">{}\n".format(protein_name)).encode('utf-8'))
            f.write(("{}\n".format(data)).encode('utf-8'))
    if len(sys.argv) != 3:
        print("args missing")
        return

    data_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), sys.argv[1])
    ana_type = int(sys.argv[2])
    if not os.path.exists(data_file):
        print("!!! err {} not exists".format(data_file))
        return

    protein_info = {}
    protein_name = ''
    with open(data_file) as f:
        for line in f.readlines():
            line = line.strip('\r\n ')
            if line.startswith('>'):
                protein_name = line[1:]
            else:
                if protein_name not in protein_info:
                    protein_info[protein_name] = []
                protein_info[protein_name].append(line)

    min_search_str_len = 99999999
    min_search_str_name = ''
    max_split_times = 0
    if ana_type > 4:
        for pk, pv in protein_info.items():
            search_str = ''.join(pv)
            search_str_len = len(search_str)
            if search_str_len < min_search_str_len:
                min_search_str_len = search_str_len
                min_search_str_name = pk
        tmp_min_search_str_split_len = min_search_str_len
        while tmp_min_search_str_split_len > 1:
            tmp_min_search_str_split_len = min(int(math.ceil(tmp_min_search_str_split_len * 0.382)),
                                               int(math.floor(tmp_min_search_str_split_len * 0.618)))
            max_split_times += 1

        for pk, pv in protein_info.items():
            search_str = ''.join(pv)
            start1 = int(len(search_str) * 0.618)
            old_split_list = [search_str[:start1], search_str[start1:]]
            new_split_list = []
            ana_type = max_split_times
            is_exit = False
            while ana_type > 0 and not is_exit:
                for item in old_split_list:
                    search_str_len = len(item)
                    start1_1 = int(search_str_len * 0.618)
                    new_split_list.append(item[:start1_1])
                    new_split_list.append(item[start1_1:])
                    start1_1_max = max(int(search_str_len * 0.618), int(math.ceil(search_str_len * 0.382)))
                    if len(item[start1_1_max:]) <= 1:
                        is_exit = True
                        break
                    if len(item[:start1_1_max]) <= 1:
                        is_exit = True
                        break
                ana_type -= 1
                if not is_exit and ana_type > 0:
                    old_split_list,new_split_list = new_split_list,old_split_list
                    new_split_list = []

            for i in range(len(new_split_list)):
                save_split_data("{}_{}.txt".format(max_split_times, i+1), new_split_list[i], pk)
    else:
        for pk,pv in protein_info.items():
            is_record_split_times = False
            tmp_split_times = 1
            search_str = ''.join(pv)
            search_str_len = len(search_str)
            if search_str_len < min_search_str_len:
                min_search_str_name = pk
                min_search_str_len = search_str_len
                is_record_split_times = True
            start1 = int(search_str_len * 0.618)
            show_protein_str = ''
            if ana_type == 1:
                save_split_data("{}_1.txt".format(ana_type), search_str[:start1], pk)
                save_split_data("{}_2.txt".format(ana_type), search_str[start1:], pk)
                search_str_len = len(search_str)
                start1_1_max = max(int(search_str_len * 0.618), int(math.ceil(search_str_len * 0.382)))
                show_protein_str = search_str[start1_1_max:]
                while len(show_protein_str) > 1:
                    tmp_index = max(int(len(show_protein_str) * 0.618), int(math.ceil(len(show_protein_str) * 0.382)))
                    show_protein_str = show_protein_str[tmp_index:]
                    tmp_split_times += 1
            if ana_type == 2:
                tmp_split_times = 2
                new_split_list = []
                for item in (search_str[:start1], search_str[start1:]):
                    search_str_len = len(item)
                    start1_1 = int(search_str_len * 0.618)
                    new_split_list.append(item[:start1_1])
                    new_split_list.append(item[start1_1:])
                    start1_1_max = max(int(search_str_len * 0.618), int(math.ceil(search_str_len * 0.382)))
                    show_protein_str = item[start1_1_max:]
                while len(show_protein_str) > 1:
                    tmp_index = max(int(len(show_protein_str) * 0.618), int(math.ceil(len(show_protein_str) * 0.382)))
                    show_protein_str = show_protein_str[tmp_index:]
                    tmp_split_times += 1
                for i in range(len(new_split_list)):
                    save_split_data("{}_{}.txt".format(ana_type, i+1), new_split_list[i], pk)
            if ana_type == 3:
                tmp_split_times = 3
                new_split_list = []
                new_new_split_list = []
                for item in (search_str[:start1], search_str[start1:]):
                    search_str_len = len(item)
                    start1_1 = int(search_str_len * 0.618)
                    new_split_list.append(item[:start1_1])
                    new_split_list.append(item[start1_1:])
                for item in new_split_list:
                    search_str_len = len(item)
                    start1_1 = int(search_str_len * 0.618)
                    new_new_split_list.append(item[:start1_1])
                    new_new_split_list.append(item[start1_1:])
                    start1_1_max = max(int(search_str_len * 0.618), int(math.ceil(search_str_len * 0.382)))
                    show_protein_str = item[start1_1_max:]
                while len(show_protein_str) > 1:
                    tmp_index = max(int(len(show_protein_str) * 0.618), int(math.ceil(len(show_protein_str) * 0.382)))
                    show_protein_str = show_protein_str[tmp_index:]
                    tmp_split_times += 1
                for i in range(len(new_new_split_list)):
                    save_split_data("{}_{}.txt".format(ana_type, i+1), new_new_split_list[i], pk)
            if ana_type == 4:
                tmp_split_times = 4
                new_split_list = []
                new_new_split_list = []
                new_new_new_split_list = []
                for item in (search_str[:start1], search_str[start1:]):
                    search_str_len = len(item)
                    start1_1 = int(search_str_len * 0.618)
                    new_split_list.append(item[:start1_1])
                    new_split_list.append(item[start1_1:])
                for item in new_split_list:
                    search_str_len = len(item)
                    start1_1 = int(search_str_len * 0.618)
                    new_new_split_list.append(item[:start1_1])
                    new_new_split_list.append(item[start1_1:])
                for item in new_new_split_list:
                    search_str_len = len(item)
                    start1_1 = int(search_str_len * 0.618)
                    new_new_new_split_list.append(item[:start1_1])
                    new_new_new_split_list.append(item[start1_1:])
                    start1_1_max = max(int(search_str_len * 0.618), int(math.ceil(search_str_len * 0.382)))
                    show_protein_str = item[start1_1_max:]
                while len(show_protein_str) > 1:
                    tmp_index = max(int(len(show_protein_str) * 0.618), int(math.ceil(len(show_protein_str) * 0.382)))
                    show_protein_str = show_protein_str[tmp_index:]
                    tmp_split_times += 1
                for i in range(len(new_new_new_split_list)):
                    save_split_data("{}_{}.txt".format(ana_type, i+1), new_new_new_split_list[i], pk)
            if is_record_split_times:
                max_split_times = tmp_split_times
    print("最大分割次数：{}".format(max_split_times))
    print("最短序列名字：>{}".format(min_search_str_name))
    print("最短序列长度：{}".format(min_search_str_len))


if __name__ == '__main__':
    main()


