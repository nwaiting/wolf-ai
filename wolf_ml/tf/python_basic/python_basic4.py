#coding=utf-8

def func1():
    """
    wsgi解析URL参数的时候:
        解析 post请求中的参数：d = parse_qs(request_body)
               # 当请求方法为POST时查询字符串被放在HTTP请求体中进行传递。它被WSGI服务器具体存放在名为wsgi.input的一个类文件环境变量中。
               # 环境变量CONTENT_LENGTH可能为空值或缺失，采用try/except来防错
                try:
                    request_body_size = int(environ.get('CONTENT_LENGTH', 0))
                except (ValueError):
                      request_body_size = 0
               request_body = environ['wsgi.input'].read(request_body_size)
               d = parse_qs(request_body)
               age = d.get('age', [''])[0] # 返回第一个age值。 ['']是默认值，如果在QUERY_STRING中没找到age则返回默认值
               hobbies = d.get('hobbies', []) # 返回一个hobbies列表。

        解析 get请求的URL参数： d = parse_qs(environ['QUERY_STRING'])
               # 解析后直接返回一个字典，每个值都是一个列表，包含了查询字符串中所有对应于该键的值
               d = parse_qs(environ['QUERY_STRING'])
               # 调用字典的get方法并传入一个key不存在时返回的默认值，这样可以在第一次显示表单时也给出合理的值
               age = d.get('age', [''])[0] # 返回第一个age值.
               hobbies = d.get('hobbies', []) # 返回一个hobbies列表.
               # 总是对用户输入进行转义来避免脚本注入
               age = escape(age)
               hobbies = [escape(hobby) for hobby in hobbies]

        environ是一个dict字典：
            response_body = ['%s: %s' % (key, value) for key, value in sorted(environ.items())]

    """

def func2():
    print('func2')
    for i in ('a',):
        print(i)
    s = """
    <!DOCTYPE html>
<!--STATUS OK--><html> <head><meta http-equiv=content-type content=text/html;charset=utf-8><meta http-equiv=X-UA-Compatible content=IE=Edge><meta content=always name=referrer><link rel=stylesheet type=text/css href=http://s1.bdstatic.com/r/www/cache/bdorz/baidu.min.css><title>百度一下，你就知道</title></head> <body link=#0000cc> <div id=wrapper> <div id=head> <div class=head_wrapper> <div class=s_form> <div class=s_form_wrapper> <div id=lg> <img hidefocus=true src=//www.baidu.com/img/bd_logo1.png width=270 height=129> </div> <form id=form name=f action=//www.baidu.com/s class=fm> <input type=hidden name=bdorz_come value=1> <input type=hidden name=ie value=utf-8> <input type=hidden name=f value=8> <input type=hidden name=rsv_bp value=1> <input type=hidden name=rsv_idx value=1> <input type=hidden name=tn value=baidu><span class="bg s_ipt_wr"><input id=kw name=wd class=s_ipt value maxlength=255 autocomplete=off autofocus></span><span class="bg s_btn_wr"><input type=submit id=su value=百度一下 class="bg s_btn"></span> </form> </div> </div> <div id=u1> <a href=http://news.baidu.com name=tj_trnews class=mnav>新闻</a> <a href=http://www.hao123.com name=tj_trhao123 class=mnav>hao123</a> <a href=http://map.baidu.com name=tj_trmap class=mnav>地图</a> <a href=http://v.baidu.com name=tj_trvideo class=mnav>视频</a> <a href=http://tieba.baidu.com name=tj_trtieba class=mnav>贴吧</a> <noscript> <a href=http://www.baidu.com/bdorz/login.gif?login&amp;tpl=mn&amp;u=http%3A%2F%2Fwww.baidu.com%2f%3fbdorz_come%3d1 name=tj_login class=lb>登录</a> </noscript> <script>document.write('<a href="http://www.baidu.com/bdorz/login.gif?login&tpl=mn&u='+ encodeURIComponent(window.location.href+ (window.location.search === "" ? "?" : "&")+ "bdorz_come=1")+ '" name="tj_login" class="lb">登录</a>');</script> <a href=//www.baidu.com/more/ name=tj_briicon class=bri style="display: block;">更多产品</a> </div> </div> </div> <div id=ftCon> <div id=ftConw> <p id=lh> <a href=http://home.baidu.com>关于百度</a> <a href=http://ir.baidu.com>About Baidu</a> </p> <p id=cp>&copy;2017&nbsp;Baidu&nbsp;<a href=http://www.baidu.com/duty/>使用百度前必读</a>&nbsp; <a href=http://jianyi.baidu.com/ class=cp-feedback>意见反馈</a>&nbsp;京ICP证030173号&nbsp; <img src=//www.baidu.com/img/gs.gif> </p> </div> </div> </div> </body> </html>
    """
    print(len(s))

def func3():
    import MySQLdb

    mysql_host='10.200.218.224'
    mysql_user='root'
    mysql_passwd='docs'
    def main():
        db = None
        try:
            db = MySQLdb.connect(host=mysql_host,user=mysql_user,passwd=mysql_passwd,db="excloud_info" )
        except Exception as ec:
            print("db connec error {0}".format(ec))
        cursor = db.cursor()
        for i in xrange(2, 1001):
            sql = "INSERT INTO conf_domain(ID,CUSID,PLANTID,DOMAIN,MUL_DOMAIN,SOURCE_CONF,SOURCE_TYPE,MAIN_UT,BACK_UT,MAIN_UC,BACK_UC,MAIN_UM,BACK_UM,HTTPS_CONF,SSL_CERT,SSL_CERT_KEY,CHECK_URL,created_time,last_modified_time) values(NULL,168,7,'test{0}.pptv.com',1,1,1,'10.200.21.117','10.200.11.149','10.200.21.117','10.200.11.149','10.200.21.117','10.200.11.149',1,'pptv.com.pem','pptv.com.key','','2018-03-13 12:47:26','2018-03-13 12:47:26')".format(i)
            try:
                cursor.execute(sql)
            except Exception as ec:
                print('mysql execute {0} error {1}'.format(sql, ec))
                db.rollback()

            if i%10 == 0:
                try:
                    db.commit()
                except Exception as ec:
                    print('mysql execute {0} error {1}'.format(sql, ec))
                    db.rollback()
                print('done {0}'.format(i))


def func4():
    s = 'xxxxxx{0}yyy{1}zzzzz{1}vvvvvv{2}'
    print(s.format(3,6,9))

def func5():
    test_map = dict()
    test_map['a'] = 'aaa'
    test_map['b'] = 4
    test_map['c'] = 6
    print(test_map.get('a', 0))
    print(test_map.get('d'))
    print(test_map.get('b') + 0.0)
    test_map['d'] += 1 # !!!!!!!!!!!报错
    print(test_map.get('d', 0) + 1)

def func6():
    """
    map函数使用
        map(function, iterable, ...)
        map()函数接收两个参数，一个是函数，一个是序列，map将传入的函数依次作用到序列的每个元素，并把结果作为新的list返回
        reduce把一个函数作用在一个序列[x1, x2, x3...]上，这个函数必须接收两个参数，reduce把结果继续和序列的下一个元素做累积计算
    """
    a = [1,2,3]
    b = [[1,],[2,],[3,]]
    print(list(map(lambda x:x+1, a))) #[2, 3, 4]
    print(list(map(lambda x:x[0]*x[0], b))) #[1, 4, 9]
    print(list(enumerate(a))) # [(0, 1), (1, 2), (2, 3)]
    # lambda 中多个参数
    print(list(map(lambda x,y,z:x*y*z, a,a,a))) #[1, 8, 27]

    print(list(map(lambda x : x * 2,range(1,10,1))))

    map(str, [1, 2, 3, 4]) # ['1', '2', '3', '4']

def func7():
    """
    sorted 函数使用
    sorted(需要排序的队列，key=排序的字段, 是否逆序)
        注：返回的队列和原理的队列不再是同一个队列 !!!!!!
    """
    a = [1,2,3,4]
    print(sorted(a, key=lambda x:x, reverse=True))
    students = [('jane', 'B', 12), ('john', 'A', 15), ('dave', 'B', 10)]
    new_students = sorted(students, key=lambda x:x[2], reverse=True)
    print(new_students, students)
    new_students[2] = 'aaaaaa'
    print(new_students, students)

    #多字段排序
    #优先按照x[1]比较，如果一样，继续比较x[0]
    max(dag[i], key=lambda x:(x[1],x[0]))

def func8():
    """
    filter函数使用
    filter(function, iterable)
    """
    import math

    new_list = filter(lambda x: x%2 == 0, range(10))
    print(list(new_list)) # [0, 2, 4, 6, 8]
    new_list = ['test', None, '', 'str', '  ', 'END']
    new_list = list(filter(lambda x:x and len(x) > 0, new_list))
    print(new_list) # ['test', 'str', '  ', 'END']
    new_list = list(filter(lambda x:math.sqrt(x) % 1 == 0, range(30)))
    print(new_list) # [0, 1, 4, 9, 16, 25]
    #map正常 可以有三个参数
    new_list = list(map(lambda x,y:(x%2==0)*(y%2==1), range(10), range(10)))

    # filter错误 多余两个参数
    new_list = list(filter(lambda x,y:(x%2==0)*(y%2==1), range(10), range(10)))
    print(new_list)

def func9():
    from functools import reduce
    """
    reduce函数使用
    reduce(function, iterable[, initializer])
    reduce把一个函数作用在一个序列[x1, x2, x3...]上，这个函数必须接收两个参数，reduce把结果继续和序列的下一个元素做累积计算，其效果就是：
    reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)
    """
    def add(x,y):
        return x+y
    print(reduce(add, range(1,6))) # 1+2+3+4+5
    print(reduce(lambda x,y:x+y, [1,2,3,4,5])) # 1+2+3+4+5
    # 这个例子要好好理解
    print(reduce(lambda x,y:x*10+y, range(5))) # 1234

def func10():
    """
    strip() 方法能用于删除开始或结尾的字符。

    lstrip() 和 rstrip() 分别从左和从右执行删除操作， 遇到不符合的则停止继续搜索
    默认情况下，这些方法会去除空白字符，但是你也可以指定其他字符
    """
    t = '-----hello====='
    print(t.strip('-=')) # hello
    t = '-------hello------'
    print(t.lstrip('-')) # hello------
    print(t.rstrip('-')) # -------hello

def func11():
    class A(object):
        def __init__(self):
            pass
    a_list = [A() for _ in range(10)]
    for i in a_list:
        print(id(i))  #队列中每个对象的地址不一样

def func12():
    import queue
    q = queue.Queue()
    q.put(0)
    q.put(1)
    q.put(2)
    while not q.empty():
        print(q.get())  # 0 1 2 先进先出

def func13():
    import socket
    print(socket.gethostname())
    print(socket.gethostbyname(socket.gethostname()))
    print(socket.gethostbyname_ex(socket.gethostname()))
    print(socket.gethostbyname_ex(socket.gethostname())[2][-1])

if __name__ == '__main__':
    #func1()
    #func2()
    #func3()
    #func4()
    #func5()
    #func6()
    #func7()
    #func8()
    #func9()
    #func10()
    #func11()
    #func12()
    #func13()
