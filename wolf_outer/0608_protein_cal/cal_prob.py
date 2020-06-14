import sys
import os
import re
from itertools import combinations, permutations

# 设置小数有效位
last_flost_bit = 10


def main():
    """
        python cal_prob.py data 1 result.txt
    """
    total_index = 0

    def save_prob_to_file(tag_flag, pro_name):
        tags_line = ''
        prob_line = ''
        dict_keys = list(search_str_probs.keys())
        dict_keys.sort()
        for k in dict_keys:
            tags_line += "{}\t".format(k)
            prob_line += "{}\t".format(search_str_probs.get(k))
        save_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), result_file)
        with open(save_file, 'ab') as f:
            if tag_flag <= 0:
                f.write(("#{}\n".format(tags_line)).encode('utf-8'))
                tag_flag += 1
            f.write((">{}\t{}\n".format(pro_name, prob_line)).encode('utf-8'))
    if len(sys.argv) != 4:
        print("args missing")
        return

    data_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), sys.argv[1])
    ana_type = int(sys.argv[2])
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

    for pk,pv in protein_info.items():
        search_str = ''.join(pv)
        search_str_probs = {}
        signal_char_str = 'ACDEFGHIKLMNPQRSTVWY'
        if ana_type == 1:
            # 计算单个频率
            total_len = len(search_str)
            for c in signal_char_str:
                res = re.findall(c, search_str)
                if res:
                    search_str_probs[c] = format(len(res)/total_len, '.{}f'.format(last_flost_bit))
                else:
                    search_str_probs[c] = 0
            save_prob_to_file(total_index, pk)
        elif ana_type == 2:
            # 二联体
            # total_len = len(search_str)*(len(search_str)+1)*(2*len(search_str)+1)/6
            total_len = len(search_str) - 1
            for cc in permutations(signal_char_str, 2):
                cc = ''.join(cc)
                res = re.findall(cc, search_str)
                if res:
                    search_str_probs[cc] = format(len(res)/total_len, '.{}f'.format(last_flost_bit))
                else:
                    search_str_probs[cc] = 0
            for cc in signal_char_str:
                cc = cc*2
                res = re.findall(cc, search_str)
                if res:
                    search_str_probs[cc] = format(len(res)/total_len, '.{}f'.format(last_flost_bit))
                else:
                    search_str_probs[cc] = 0
            save_prob_to_file(total_index, pk)
        elif ana_type == 3:
            # 三联体
            # total_len = (len(search_str)*(len(search_str)+1)/2)*(len(search_str)*(len(search_str)+1)/2)
            total_len = len(search_str) - 2
            items = ['AGV','ILFP','YMTS','HNQW','RK','DE','C']
            new_items = [''.join(cc) for cc in permutations(items, 2)] + [cc*2 for cc in items]
            last_items = []
            for one in new_items:
                for two in items:
                    last_items.append(one+two)
            for item in last_items:
                res = re.findall(item, search_str)
                if res:
                    search_str_probs[item] = format(len(res)/total_len, '.{}f'.format(last_flost_bit))
                else:
                    search_str_probs[item] = 0
            save_prob_to_file(total_index, pk)
        else:
            print("args err {}".format(sys.argv))
        total_index += 1


if __name__ == '__main__':
    main()


