#coding=utf-8

import re

def parse_txt(input, output):
    total_map = {}
    with open(input_file, 'rb') as finput:
        with open(output_file, 'wb') as foutput:
            for line in finput.readlines():
                line = line.strip().decode()
                first_index = line.find(' ')
                if first_index != -1:
                    first_pref = line[:first_index]
                    res = first_pref.split('.')
                    for item in res:
                        if item.isdigit():
                            total_map[first_pref] = line[first_index+1:]
                            foutput.write(('{0} {1}\n'.format(first_pref, line[first_index+1:])).encode())
                            break

if __name__ == '__main__':
    input_file = 'outer/pdf2index/result1.txt'
    output_file = 'outer/pdf2index/output_data'
    parse_txt(input_file, output_file)
