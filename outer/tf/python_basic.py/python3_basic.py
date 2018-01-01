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

if __name__ == '__main__':
    import sys
    print(len(sys.argv), sys.argv[0])
    #func1()
    func2()
