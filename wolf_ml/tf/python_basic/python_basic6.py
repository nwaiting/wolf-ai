#coding=utf-8


def func1():
    """
        f = open("a.txt", "r")
        f.tell() #查看在文件中的当前位置
        f.seek(8, 0) #表示从文件开始处移动到文件的X字节处,第二个参数：0表示从文件开始处移动到文件的x处，1表示相对于当前位置移动到X字节处，2表示相对于文件末尾的位置
    """
    import os
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'a.txt')
    with open(file, 'r') as fd:
        fd.seek(1)
        print(fd.read())

if __name__ == '__main__':
    func1()
