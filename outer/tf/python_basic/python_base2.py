#coding=utf-8

def func1():
    """
        uwsgi 直接启动的脚本
        ./uwsgi --wsgi-file uwsgi_server.py --master -s /tmp/uwsgi.sock -p 1 --uid jiexu --gid jiexu --module wsgi -d /dev/null
    """
    from cgi import parse_qs, escape

    def application(environ, start_response):
        try:
            request_body = environ['wsgi.input'].read()
            d = parse_qs(request_body)

            # 获取数据
            age = d.get('age', [])
            hobbies = d.get('hobbies', [])
            response_status = '200 OK'
            response_headers = [('Content-Type', 'text/plain')]
            with open('/home/jiexu/work/wsgi_async/proxy/uwsgi/test.log', 'ab+') as f:
                pass
        except Exception as e:
            print("Exception {}".format(e))
        start_response(response_status, response_headers)
        return [environ["REQUEST_URI"], environ["QUERY_STRING"]]

def func2():
    import time
    now = time.time()
    print(now, now*1000)

def func3():
    """
        list相关操作
    """
    a = [[1,2,3],[4,5,6],[7,8,9]]
    b = [i[0] for i in a]
    print(b)

    list_a = ['a','b',1,2,3]
    print([list_a[0]+'-'+list_a[1]]+list_a[2:])

def func4():
    """
    isdigit()
    判断是不是数字
    但是只能判断 整数 如果需要判断小数的话 需要自己做处理
    """
    import re
    s1 = '1234'
    s2 = '12.34'
    s3 = '1.2.3 好不好'
    s4 = '1.'
    print(s1.isdigit())
    print(s2.isdigit())
    patt = re.compile(r"^(-?\d+)(\.\d*)?(\.\d*)?")
    patt = re.compile(r"^(-?\d+)(\.\d*)+?")
    patt = re.compile(r"^(-?\d+)((\.\d*){1,})?")
    res = re.match(patt, s3)
    print(res.group())
    print(re.match(patt, s4).group())

if __name__ == '__main__':
    #func1()
    #func2()
    #func3()
    func4()
