#coding=utf-8

def parse_str(input, output, filter_list):
    with open(input_file, 'rb') as finput:
        with open(out_file, 'wb') as foutput:
            for line in finput.readlines():
                line = line.strip().decode()
                res = line.split(';')
                write_line = ''
                for item in res:
                    dd = [item for i in filter_list if item.endswith(i)]
                    if dd:
                        write_line += item + ';'
                if write_line:
                    write_line += '\n'
                    foutput.write(write_line.encode())

input_file = 'outer/CoRelationWithWordType/CoRelationWithWordType.txt'
out_file = 'outer/CoRelationWithWordType/CoRelationWithWordType.result'
filters = ['n_jb','n_zz','n_zd','n_qg']
parse_str(input_file, out_file, filters)
