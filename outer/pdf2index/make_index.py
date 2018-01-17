#coding=utf-8

import re

def parse_txt(input, output):
    total_map = {}
    with open(input_file, 'rb') as finput:
        with open(output_file, 'wb') as foutput:
            # 对输入文件每一行遍历进行处理
            for line in finput.readlines():
                line = line.strip().decode()
                first_index = line.find(' ')
                if first_index != -1:
                    # 找到空格分开的第一个字段
                    first_pref = line[:first_index]
                    # 对第一个字段进行判断 如果是小数的话 使用小数点.进行分割 然后判断分割后的是不是数字 如果是数字 那么作为一个目录的key
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
