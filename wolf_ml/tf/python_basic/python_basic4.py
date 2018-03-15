#coding=utf-8

def func1():
    """
    wsgi解析URL参数的时候:
        解析 post请求中的参数：d = parse_qs(request_body)
        解析 get请求的URL参数： d = parse_qs(environ['QUERY_STRING'])
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

if __name__ == '__main__':
    #func1()
    #func2()
    #func3()
    #func4()
    func5()
