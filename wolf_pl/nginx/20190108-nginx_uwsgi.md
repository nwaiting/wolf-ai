## nginx - uwsgi
- **概述：**
>
>
>
>
>
>
>
>

- **搭建一个简单的nginx+uwsgi的web服务：**
>       1、nginx配置：
>         location /GetAppConfig.s {
>            include uwsgi_params;
>            uwsgi_pass unix:/var/t.sock;
>         }
>       2、启动uwsgi：
>           uwsgi --master --module wsgi --wsgi-file t.py -s /var/t.sock -p 2 --uid pplive -d /home/logs/wsgi/uwsgi.log
>
>           如果用uwsgi.ini启动的话，uwsgi.ini配置：
>               如果想实现下面的功能，那么，在uWSGI的启动配置中，去掉”wsgi-file”项，并加上下面的项：
>               [uwsgi]
>                   ...
>                   mount=/myapp=server.py      #参数表示将”/myapp”地址路由到”server.py”中
>                   manage-script-name=true     #参数表示启用之前在Nginx里配置的”SCRIPT_NAME”参数
>             对应的nignx.conf里面的配置：
>               location /myapp {
>                   include uwsgi_params;
>                   uwsgi_param SCRIPT_NAME /myapp;     #定义了一个uWSGI参数”SCRIPT_NAME”，值为应用的路径”/myapp”。接下来，在uWSGI的启动配置中，去掉”wsgi-file”项
>                   uwsgi_pass unix:/var/t.sock;
>                   }
>
>
>       3、t.py逻辑处理
>           def application(env, start_response):
>               req_uri = env["PATH_INFO"]
>               response_body = req_uri
>               response_status = '200 OK'
>               response_header = [('Cache-Control', 'no-cache'),
>                                   ('Connection', 'close'),
>                                   ('Content-Length', str(len(response_body)))]
>               start_response(response_status, response_header)
>               return response_body
>

- **注：**
>       如果uwsgi的子进程重启，并不会使改动的py脚本生效，仅只是重启了uwsgi的子进程
>
>
>

- **待续：**
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
