



"""
Flask-cors解决跨域的问题：
    跨域：
        跨域(跨源)是指浏览器从一个源的网页去请求另一个源，源指的是域名、端口、协议，只要其中一个不一样那么就是跨域请求
        以下都属于跨域问题
        域名：
            主域名不同: http://www.baidu.com/index.html –> http://www.sina.com/test.js
            子域名不同: http://www.666.baidu.com/index.html –> http://www.555.baidu.com/test.js
            域名和域名ip: http://www.baidu.com/index.html –>http://180.149.132.47/test.js
        端口：
            http://www.baidu.com:8080/index.html–> http://www.baidu.com:8081/test.js
        协议：
            http://www.baidu.com:8080/index.html–> https://www.baidu.com:8080/test.js

    为什么要考虑跨域问题
        因为Ajax不能跨域, 一旦客户端和服务端的不在一台服务器, 则需要考虑跨域访问的问题
        上线之前会出现很多跨域的问题

    同源策略
        同源策略是浏览器的一项最为基本同时也是必须遵守的安全策略。
        同源策略的存在，限制了“源”自A的脚本只能操作“同源”页面的DOM，“跨源”操作来源于B的页面将会被拒绝。
        所谓的“同源”，必须要求相应的URI的域名、端口、协议均是相同的。

    参考：
        https://www.jianshu.com/p/20f0dac076d3   Flask-cors跨域
"""




if __name__ == '__main__':
    pass
