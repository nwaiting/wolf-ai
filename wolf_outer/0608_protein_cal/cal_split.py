import sys
import os


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
    for pk,pv in protein_info.items():
        search_str = ''.join(pv)
        search_str_len = len(search_str)
        start1 = int(search_str_len * 0.618)
        show_protein_str = ''
        if ana_type == 1:
            save_split_data("{}_1.txt".format(ana_type), search_str[:start1], pk)
            save_split_data("{}_2.txt".format(ana_type), search_str[start1:], pk)
            show_protein_str = search_str[start1:]
        if ana_type == 2:
            new_split_list = []
            for item in (search_str[:start1], search_str[start1:]):
                search_str_len = len(item)
                start1_1 = int(search_str_len * 0.618)
                new_split_list.append(item[:start1_1])
                new_split_list.append(item[start1_1:])
                show_protein_str = item[start1_1:]
            for i in range(len(new_split_list)):
                save_split_data("{}_{}.txt".format(ana_type, i+1), new_split_list[i], pk)
        if ana_type == 3:
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
                show_protein_str = item[start1_1:]
            for i in range(len(new_new_split_list)):
                save_split_data("{}_{}.txt".format(ana_type, i+1), new_new_split_list[i], pk)
        if ana_type == 4:
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
                show_protein_str = item[start1_1:]
            for i in range(len(new_new_new_split_list)):
                save_split_data("{}_{}.txt".format(ana_type, i+1), new_new_new_split_list[i], pk)
        print("最大分割次数：{}".format(ana_type))
        print("序列名字：>{}".format(protein_name))
        print("最短序列长度：{}".format(len(show_protein_str)))


if __name__ == '__main__':
    main()


