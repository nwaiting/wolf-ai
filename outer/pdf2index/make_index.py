#coding=utf-8

import re

def parse_txt(input, output):
    total_map = {}
    with open(input_file, 'rb') as finput:
        with open(output_file, 'wb') as foutput:
            # 对输入文件每一行遍历进行处理
            last_line = ''
            last_line_flag = 0
            map_key = ''
            map_value = ''
            patt_line = re.compile(r"^(-?\d+)((\.\d*){1,})? ")
            patt_pre = re.compile(r"^(-?\d+)((\.\d*){1,})?")

            for line in finput.readlines():
                line = line.strip().decode()
                res = re.match(patt_line, line) or re.match(patt_pre, line)
                if res:
                    if map_key and map_value:
                        foutput.write(('{0} {1}\n'.format(map_key, map_value)).encode())
                        map_key, map_value = '', ''
                    map_key = res.group(0)
                    first_index = line.find(' ')
                    if first_index != -1:
                        map_value += ' ' + line[first_index+1:]
                    else:
                        map_value += ' ' + line.replace(map_key, '')
                else:
                    map_value += ' ' + line
            if map_key and map_value:
                foutput.write(('{0} {1}\n'.format(map_key, map_value)).encode())

                """
                if re.match(patt_line, line):
                    first_index = line.find(' ')
                    if first_index != -1:
                        # 找到空格分开的第一个字段
                        last_line_flag = 0
                        last_line = ''
                        first_pref = line[:first_index]
                        # 对第一个字段进行判断 如果是小数的话 使用小数点.进行分割 然后判断分割后的是不是数字 如果是数字 那么作为一个目录的key
                        res = first_pref.split('.')
                        for item in res:
                            if item.isdigit():
                                total_map[first_pref] = line[first_index+1:]
                                foutput.write(('{0} {1}\n'.format(first_pref, line[first_index+1:])).encode())
                                break
                    last_line_flag = 0
                    last_line = ''
                elif re.match(patt_pre, line):
                    last_line_flag += 1
                    last_line = line
                else:
                    if last_line_flag == 1 and line and re.match(patt_pre, last_line):
                        foutput.write(('{0} {1}\n'.format(last_line, line)).encode())
                        last_line_flag = 0
                        last_line = ''
                """

if __name__ == '__main__':
    input_file = 'outer/pdf2index/struct.txt'
    output_file = 'outer/pdf2index/output_data'
    parse_txt(input_file, output_file)
