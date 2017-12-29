#coding=utf-8

import json
import sys

if __name__ == '__main__':
    with open('a.txt', 'rb') as fd:
        json_con = json.load(fd)
        length = len(sys.argv)
        first_pra = sys.argv[1]
        second_pra = sys.argv[2]
        if length == 3:
            print json_con[first_pra][second_pra]
        elif length == 4:
            third_pra = sys.argv[3]
            print json_con[first_pra][second_pra][third_pra]
