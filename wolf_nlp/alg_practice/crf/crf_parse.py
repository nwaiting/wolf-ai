#coding=utf8

"""
crf分词：
    参考：http://x-algo.cn/index.php/2016/02/27/crf-of-chinese-word-segmentation/
"""

import sys
import os
import codecs

base_dir = os.path.dirname(os.path.realpath(__file__))
input_file_name = os.path.join(base_dir, 'people_daily.txt')
train_file_name = os.path.join(base_dir, 'train.data')
test_file_name = os.path.join(base_dir, 'test.data')

train_file = open(train_file_name, 'wb')
test_file = open(test_file_name, 'wb')

def savefile(save_train_flag, item, item_tag, tag):
    if item:
        word_length = len(item)
        tag_list = []
        if tag == 4:
            if word_length == 1:
                tag_list.append('S')
            elif word_length == 2:
                tag_list = ['B','E']
            elif word_length >= 3:
                tag_list = ['B']
                for _ in range(word_length-2):
                    tag_list.append('M')
                tag_list.append('E')
        elif tag == 6:
            if word_length == 1:
                tag_list = ['S']
            elif word_length == 2:
                tag_list = ['B','E']
            elif word_length == 3:
                tag_list = ['B','M','E']
            elif word_length == 4:
                tag_list = ['B', 'M1', 'M', 'E']
            elif word_length >= 5:
                tag_list = ['B', 'M1', 'M2']
                for _ in range(word_length-4):
                    tag_list.append('M')
                tag_list.append('E')

        res = ''
        for i in range(word_length):
            res += '{0}\t{1}\t{2}\n'.format(item[i], item_tag, tag_list[i])
        if save_train_flag:
            train_file.write(res.encode('utf8'))
        else:
            test_file.write(res.encode('utf8'))

def convertTag(tag):
    input_pf = None
    try:
        input_pf = codecs.open(input_file_name, mode='r', encoding='utf-8')
    except Exception as ec:
        print('open error {0}'.format(ec))

    save_tag_index = 0
    for line in input_pf.readlines():
        if line:
            save_tag_index += 1
            line = line.strip('\t\r\n ')
            lines = line.split()
            for word in lines:
                if word:
                    left_index = word.find('[')
                    if left_index != -1:
                        word = word[left_index+1:]
                    right_index = word.find(']')
                    if right_index != -1:
                        word = word[:right_index]
                    word_list = word.split('/')
                    if word_list[1] == 'nr':
                        for item in word_list[0].split('.'):
                            savefile(save_tag_index%10!=0, item, word_list[1], tag)
                    elif word_list[1] != 'w':
                        savefile(save_tag_index%10!=0, word_list[0], word_list[1], tag)
    input_pf.close()

if __name__ == '__main__':
    tag = 4
    if len(sys.argv) == 2:
        tag = sys.argv[1]
    convertTag(tag)
    train_file.close()
    test_file.close()
