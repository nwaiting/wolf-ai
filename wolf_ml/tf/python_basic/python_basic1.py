#coding=utf-8

def func1():
    """
    zip(a,b) 中以最短的列表作为基准，当a的长度比b长时，最多输出a的长度个数据
    """
    a = [1,2,3]
    b = [11,12,13]
    """
    1、直接操作
    """
    abc = zip(a,b)
    print(list(abc))

    """
    2、遍历
    """
    for i,j in zip(a,b):
        print(i,j)

    """
    3、复原
    """
    ij = zip(a,b)
    res = zip(*ij)
    print(list(res))

def func2():
    """
    文件和字符串的json操作
    """
    import json
    # 文件操作
    with open('a.txt', 'rb') as fd:
        contents = json.load(fd)
        print(contents[key])

    #字符串操作
    json_string = '{"a":0, "b":1}'
    contents = json.loads(json_string)
    print(contents['a'])

    #文件操作 dict转成str然后存入到文件中
    jsong_string = ''
    with open('a.txt', 'rb') as fd:
        json.dump(json_string, fd)

    #字符串操作 json转成字符串
    contents = json.dumps(json_string)

def func3():
    """
    py2和py3的sorted()函数差别
    Python2中的自定义布尔函数cmp=custom_cmp(x, y)由Python3中的key=custom_key(x)代替
    python3 sorted取消了对cmp的支持
    sorted(iterable, key=None, reverse=False)
        reverse是一个布尔值。如果设置为True，列表元素将被倒序排列，默认为False
        key接受一个函数，这个函数只接受一个元素，默认为None
    """
    teacher_index = {'701011': {'ZHU': ['7010115060']}, '701012': {'WANG': []}, '701021': {'TAN': []}, '701022': {'YANG': []}, '701031': {'SUN': []}, '701032': {'QIAN': []}, '701041': {'LIU': []}, '701042': {'SUN': []}, '701051': {'ZHANG': []}, '701052': {'TANG': []}}
    for i,j in teacher_index.items():
        print(j, len(list(j.values())[0]))
    res = sorted(teacher_index.items(), key=lambda x:len(list(x[1].values())[0]),reverse=False)
    print(res)

def func4():
    import sched
    import time
    scher = sched.scheduler(time.time, time.sleep)
    def inner_func4():
        print('inner_func4')
        scher.enter(1, 1, inner_func4)
    def inner_fun4_2():
        print('inner_fun4_2')
        scher.enter(1, 1, inner_fun4_2)

    scher.enter(1, 1, inner_func4)
    scher.enter(1, 1, inner_fun4_2)
    scher.run()

def func5():
    """
    python3中：
    bytes -> str decode()
    str -> bytes encode()
    """
    str_str = 'hello'
    print(type(str_str), str_str)
    print(type(str_str.encode()), str_str.encode())
    bytes_str = b'hello'
    print(type(bytes_str), bytes_str)
    print(bytes_str.decode())

def func6():
    """
    输出py版本
    """
    import platform
    print(platform.python_version())

def func7():
    dict_a = {'a':1,'b':2, 'c':3}
    print(type(dict_a).__name__)
    for inst in dict_a:
        print(type(inst), inst)  #输出a b c
    for inst in dict_a.items():
        print(inst)

def func8():
    """
    operator.itemgetter函数
    operator模块提供的itemgetter函数用于获取对象的哪些维的数据，参数为一些序号（即需要获取的数据在对象中的序号）

    sorted函数也可以进行多级排序，例如要根据第二个域和第三个域进行排序，可以这么写：
    sorted(students, key=operator.itemgetter(1,2))  即先根据第二个域排序，再根据第三个域排序
    """
    from operator import itemgetter
    a = [1,2,3]
    c = [[1,2,3],[2,3,4],[3,4,5]]
    b = itemgetter(0)
    print(b(a))
    print(b(c))

def func9():
    """
    表格处理
    """

    """
    from texttable import Texttable, get_color_string, bcolors
    table = Texttable()
    table.set_cols_align(["l", "r", "c"])
    table.set_cols_valign(["t", "m", "b"])
    table.add_rows([ [table.get_color_string(bcolors.GREEN, "Name Of Person"), "Age", "Nickname"],
                 ["Mr\nXavier\nHuon", 32, "Xav'"],
                 [table.get_color_string(bcolors.BLUE,"Mr\nBaptiste\nClement"), 1, table.get_color_string(bcolors.RED,"Baby")] ])
    print(table.draw() + "\n")

    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.set_cols_dtype(['t',  # text
                          'f',  # float (decimal)
                          'e',  # float (exponent)
                          'i',  # integer
                          'a']) # automatic
    table.set_cols_align(["l", "r", "r", "r", "l"])
    table.add_rows([["text",    "float", "exp", "int", "auto"],
                    ["abcd",    "67",    654,   89,    128.001],
                    ["efghijk", 67.5434, .654,  89.6,  12800000000000000000000.00023],
                    ["lmn",     5e-78,   5e-78, 89.4,  .000000000000128],
                    ["opqrstu", .023,    5e+78, 92.,   12800000000000000000000]])
    print(table.draw())
    """

    from texttable import Texttable
    table = Texttable()
    table.set_cols_align(["l", "r", "c"])
    table.set_cols_valign(["t", "m", "b"])
    table.add_rows([["Name", "Age", "Nickname"],
                    ["Mr\nXavier\nHuon", 32, "Xav'"],
                    ["Mr\nBaptiste\nClement", 1, "Baby"],
                    ["Mme\nLouise\nBourgeau", 28, "Lou\n \nLoue"]])
    print(table.draw() + "\n")

    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.set_cols_dtype(['t',  # text
                          'f',  # float (decimal)
                          'e',  # float (exponent)
                          'i',  # integer
                          'a']) # automatic
    table.set_cols_align(["l", "r", "r", "r", "l"])
    table.add_rows([["text",    "float", "exp", "int", "auto"],
                    ["abcd",    "67",    654,   89,    128.001],
                    ["efghijk", 67.5434, .654,  89.6,  12800000000000000000000.00023],
                    ["lmn",     5e-78,   5e-78, 89.4,  .000000000000128],
                    ["opqrstu", .023,    5e+78, 92.,   12800000000000000000000]])
    print(table.draw())

def func10():
    """
    字符串操作：
        删除字符 translate
        先制作翻译表，然后删除相关字符
    """
    input_str = 'abcd!@#$1234%^&*5678'
    out_str = 'abcd!@#$1234%^&*5678'
    str.maketrans(input_str, out_str)
    print(input_str.translate('ab'))

    print(input_str.replace('a',''))

def func11():
    import urlparse
    print(urlparse.urljoin('http://baidu.com/home', 'test')) #http://baidu.com/test

def func12():
    """
        参数 解析
        1、sys.argv
        2、from optparse import OptionParser
    """
    import sys
    print(len(sys.argv), sys.argv[0])

    from optparse import OptionParser
    opt = OptionParser()
    opt.add_option('-d',
                    action="store_true",
                    dest="is_daemon",
                    default=False,
                    help="run the scripts daemon")
    opts, args = opt.parse_args()
    if args.is_daemon:
        pass

if __name__ == '__main__':
    #func1()
    #func2()
    #func4()
    #func5()
    #func6()
    #func7()
    #func8()
    #func9()
    #func10()
    #func11()
    #func12()
