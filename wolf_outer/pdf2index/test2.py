#!/usr/bin/env python
# encoding: utf-8
"""
@file: structinformation.py
@说明： 输入待解析的pdf文件名
"""
import sys
from io import StringIO
import importlib
importlib.reload(sys)
import math
from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams,LTImage,LTText,LTTextLineVertical,LTFigure,LTChar,LTAnon,LTTextLine
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
import matplotlib.pyplot as plt
import re
import os
import linecache
import pickle as pic
'''
 解析pdf 文本，保存到txt文件中
'''
def PDFstruct(input_file):
#------------------利用pdfminer进行文本解析---------------------------------------
#    fp = open(input_file, 'rb') # 以二进制读模式打开
    fp = open(input_file, 'rb') # 以二进制读模式打开
    #用文件对象来创建一个pdf文档分析器
    praser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器 与文档对象
    praser.set_document(doc)
    doc.set_parser(praser)

    # 提供初始化密码
    # 如果没有密码 就创建一个空的字符串
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
#    if not doc.is_extractable:
    if False:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf 资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)
#         循环遍历列表，每次处理一个page的内容
#        for page in doc.get_pages(): # doc.get_pages() 获取page列表
        fff = []
        stinf = []
        for i, page in enumerate(doc.get_pages()):
#            with open(r'struct.txt','a', encoding='utf-8') as ff:
                comp = None
                textline = []
                threshold = 10.5
#                for i ==0:
#                    print(page)
                interpreter.process_page(page)
            # 接受该页面的LTPage对象
                layout = device.get_result()
                res1 = []
                res2 = []
                res3 = []
                res4 = []
                res5 = []
                res6 = []
                ff = []
                if i == 0:
                    for x in layout:
                        for y in x:
                            if (isinstance(y, LTChar)) :
#----------------------------------单独建立文件夹提取封面信息数据保存至struct6.txt-------------------------
#-----------------------------------------清空首页信息文件内容--------------------------------------------
                                    res = y.get_text()

                                    fz = []#存首页信息
                                    if     200 >  y.x0 > 75 and 800 > y.y0 >770  : #按照坐标判断ICS号
                                        res1.append(res)
#                                        f1.write(res1)
#                                        print (f1)

                                    elif     550 > y.x0 > 380 and 661 > y.y0 >641  : #GB号
                                        res2.append(res)
#                                        print (res2)

                                    elif   600 > y.x0 > 100 and 500 > y.y0 >350  : #按照坐标判断标准名称
                                        res3.append(res)

                                    elif   112 > y.x0 > 53 and 120 > y.y0 >90  : #按照坐分布日期
                                        res4.append(res)
#                                        print (res1)

                                    elif   498 > y.x0 > 438 and 120 > y.y0 >90  : #按照坐标查找实施日期
                                        res5.append(res)
#                                        print (res1)

                                    elif   408 > y.x0 > 100 and 80> y.y0 >20  : #按照坐标查找发布单位
                                        res6.append(res)

                        if res6 :
                            pass
#                            print('正在解析···')
                        else :
                            print('waring!!! 文件非文本格式PDF，请更换文件重新解析')
                            sys.exit
                            return


                        res1.insert(0,'0 ISC号: ')
                        res1 = ''.join(res1)
                        res1 = res1.strip().split('::')
                        res2.insert(0,'0 GB号: ')
                        res2 = ''.join(res2)
                        res2 = res2.strip().split('::')
                        res3.insert(0,'0 标准名称: ')
                        res3 = ''.join(res3)
                        res3 = res3.strip().split('::')
                        res4.insert(0,'0 发布日期: ')
                        res4 = ''.join(res4)
                        res4 = res4.strip().split('::')
                        res5.insert(0,'0 实施日期: ')
                        res5 = ''.join(res5)
                        res5 = res5.strip().split('::')
                        res6.insert(0,'0 发布单位: ')
                        res6 = ''.join(res6)
                        res6 = res6.strip().split('::')
                        res7 = ['0 目录和标题']
                        fz = [res1,res2,res3,res4,res5,res6,res7]
#                        print (fz)
#                        if res6:
#                            print('正在解析···')
#                        else:
#                            print('waring!!! 文件非文本格式PDF，请更换文件重新解析')
#                            sys.exit
##-------------------------------------保存除了首页的信息至struct.txt-----------------------------------------
                else:
##            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
                    for x in layout:
                        for y in x:
                            if (isinstance(y, LTChar)):
                                    results = y.get_text()
########按坐标将每行文字排列起来
                                    if comp == None:
                                        comp = y.y0
                                        textline.append(results+' '+str(y.y0))
                                    elif results == '.' or results == '  ':
                                        comp = comp
                                        textline.append(results+ ' '+str(y.y0))
                                    elif abs(comp - y.y0) < threshold and results !='…' :
                                        textline.append(results+' '+str(y.y0))
#                                        print(textline)
                                    else:
#                                        ff.witelines('\n')
                                        ff.append(textline)
                                        comp = y.y0
                                        textline = [results]

                fff.append(ff)
                for j in fff:
    #                   print(book.index(i))
                    temp = None
                    last_line = None
                    for lin in j:
                        line = ''.join(lin)
                        line = line.strip()
    #                   print(line)
                        if re.match(re.compile(r"[图][0-9]{1}"),line):
                            print('before ===================================================================', line)
                            if last_line:
                                #找到上一行
                                print(last_line)
                            print('last ====================================================================', last_line)
                        else:
                            temp = line
                            #print(temp)
                        last_line = line
#                            print (y.y0)
#                            print (y.y1)
#                        elif re.match(re.compile(r"…[(.*)]"), line):
#                            print(line)
#                            print (y.y0)

#                break
#
###----------------------------------------------------------------------------------------------------------------
##----------------------------将首页信息与正文内容合并--------------------------------------------------------------
#
#    total_map = []
###----将所有内容存成list-----
#    book = []
    books = []
    book = fz + fff
    for i in book:
#        print(book.index(i))
        for lin in i:
            line = ''.join(lin)
            line = line.strip()
            first_index = line.find(' ')
            ex_index1 = line.find('图') #滤掉图名
            ex_index2 = line.find('表') #滤掉表头
            ex_index3 = line.find('———') #滤掉"——"
##            ex_index4 = line.find('GB')
##            ex_index5 = line.find('I')
            if first_index != -1 and ex_index1 == -1 and ex_index2 == -1 and ex_index3 == -1 and line[0]!='G' and line[0]!='I' :
##                first_pref = line[:first_index]+str(':')
                first_pref = line[:first_index]
                res = first_pref.split('.')
                for item in res:
                    if item.isdigit() and ( book.index(i) <= 7 or len(line[first_index+1:]) < 100) :
                        line1 = line[first_index+1:]
                        first_pref = line[:first_index]+str(':')
                        if item.isdigit() and book.index(i) > 7 and  len(line[first_index+1:]) > 16 :
                            line1 = str('Null')
                            first_pref = line[:first_index]+str(':')
#                            total_map = first_pref + line1
                        elif book.index(i) <= 7:
                            line1 = line[first_index+1:]
                            first_pref = line[:first_index]
#                            total_map = first_pref  + line1
#                            print (total_map)
#                               elif count > 7 and ex_index4 == -1 and ex_index5 == -1:
#                                   line1 = line[first_index+1:first_index+16]
                        else  :
                            line1 = line[first_index+1:first_index+16]
                            first_pref = line[:first_index]+str(':')
                        total_map = line1
                        total_map =  first_pref + line1
                        stinf = total_map.strip().split()
                books.append(stinf)
#                print (type(books))

###-------------------------------------以层次结构字典存储结构化信息---------------------------------------------------
    book_struct = {}
    directories = {}
    headers = {}
#    print(books)
    for i in books:
        line = ''.join(i)
        line = line.strip()
        if line.startswith('0'):
            line = line[1:].strip()
            res = line.split(':')
#            print(res)
            if len(res) == 2:
#                print('k {} v {}'.format(res[0], res[1]))
                book_struct[res[0]] = res[1]
#                print(book_struct)
        elif re.match(r"^.*?\d$", line):
            res = line.split(':')
#            print(res)
            if len(res) == 2:
                ress = re.findall(r'\d+', res[1])
                if ress:
                    k = res[1].replace(ress[0], '').strip()
                    v = ress[0].strip()
#                    print('k {} v {}'.format(k, v))
                    directories[k] = v
        else:
            res = line.split(':')
            if len(res) == 2:
                headers[res[0]] = res[1].strip()
    book_struct['目录'] = directories
    book_struct['章节标题'] = headers
#    print (book_struct)
    return book_struct

##---------------------------------------------------输入输出----------------------------------------------------
if __name__ == '__main__':
    input_file = '7.pdf'
    PDFstruct(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file))
