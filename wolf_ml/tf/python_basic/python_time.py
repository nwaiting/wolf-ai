#coding=utf-8


def func1():
    import datetime
    import time
    res = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(res)
    print(datetime.datetime.now())

    ts = int(time.time())
    res = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
    print(res)

if __name__ == '__main__':
    func1()
