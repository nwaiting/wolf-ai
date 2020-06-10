import sys
import os
import re
from itertools import combinations, permutations


def main():
    """
        python cal_prob.py data 1 result.txt
    """
    if len(sys.argv) != 4:
        print("args error")

    data_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), sys.argv[1])
    ana_type = sys.argv[2]
    result_file = sys.argv[3]
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
    search_str_probs = {}
    signal_char_str = 'ACDEFGHIKLMNPQRSTVWY'
    if ana_type == 1:
        # 计算单个频率
        total_len = len(signal_char_str)
        for c in signal_char_str:
            res = re.findall(c, search_str)
            if res:
                search_str_probs[c] = len(res)/total_len
            else:
                search_str_probs[c] = 0
    elif ana_type == 2:
        # 二联体 todo total_len
        total_len = len(list(permutations(search_str, 2)))
        for cc in permutations(signal_char_str, 2):
            res = re.findall(''.join(cc), search_str)
            if res:
                search_str_probs[cc] = len(res)/total_len
            else:
                search_str_probs[cc] = 0
    elif ana_type == 3:
        # 三联体
        pass


if __name__ == '__main__':
    # main()

    s1 = '123'
    print([''.join(i) for i in permutations(s1, 2)])


