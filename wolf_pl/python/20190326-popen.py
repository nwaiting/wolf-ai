#coding=utf-8

"""
    popen
        popen.kill() 仅仅杀死了终端，但由终端启动的服务进程并没有杀死
        使用popen执行系统命令时，结果popen开启的进程，不要使用popen.kill()了，使用os.killpg()！
        PS：os.kill()，这个也不好使，也只是杀死一个终端进程而已，并没有杀死由终端开启的子进程
"""


def main():
    pass







if __name__ == '__main__':
    main()
