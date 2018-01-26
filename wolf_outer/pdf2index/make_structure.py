#coding=utf-8

import os,re

def make_struct(filename):
    book_struct = {}
    directories = {}
    headers = {}
    with open(filename, 'rb') as fd:
        for line in fd.readlines():
            line = line.strip().decode()
            if line.startswith('0'):
                line = line[1:].strip()
                res = line.split(':')
                if len(res) == 2:
                    print('k {} v {}'.format(res[0], res[1]))
                    book_struct[res[0]] = res[1]
            elif re.match(r"^.*?\d$", line):
                res = line.split(':')
                if len(res) == 2:
                    ress = re.findall(r'\d+', res[1])
                    if ress:
                        k = res[1].replace(ress[0], '').strip()
                        v = ress[0].strip()
                        print('k {} v {}'.format(k, v))
                        directories[k] = v
            else:
                res = line.split(':')
                if len(res) == 2:
                    headers[res[0]] = res[1].strip()
        book_struct['目录'] = directories
        book_struct['章节标题'] = headers
    return book_struct

if __name__ == '__main__':
    file_name = 'output_data.new.data'
    new_file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), file_name)
    res = make_struct(new_file_name)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'aaaa.data'), 'wb') as fd:
        #for k,v in res.items():
        #    fd.write(('{0}:{1}\n'.format(k,v)).encode())
        fd.write(("{}".format(res)).encode())
