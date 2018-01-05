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

if __name__ == '__main__':
    import sys
    print(len(sys.argv), sys.argv[0])
    #func1()
    #func2()
    #func4()
    #func5()
    func6()
