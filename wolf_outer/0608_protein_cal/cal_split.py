import sys
import os


def main():
    """
        python cal_split.py data 1
    """
    def save_prob_to_file():
        pass
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
    search_str = ''.join(protein_info[protein_name])
    search_str_len = len(search_str)
    start1 = int(search_str_len * 0.618)
    start1_1 = 0
    start1_1_1 = 0
    show_str = ''
    if ana_type >= 1:
        show_str = search_str[start1:]
    if ana_type >= 2:
        start1_1 = start1 + int((search_str_len - start1) * 0.618)
        show_str = search_str[start1_1:]
    if ana_type >= 3:
        start1_1_1 = start1_1 + int((search_str_len - start1_1) * 0.618)
        show_str = search_str[start1_1_1:]
    if ana_type >= 4:
        start1_1_1_1 = start1_1_1 + int((search_str_len - start1_1_1) * 0.618)
        show_str = search_str[start1_1_1_1:]
    print(show_str)


if __name__ == '__main__':
    main()


