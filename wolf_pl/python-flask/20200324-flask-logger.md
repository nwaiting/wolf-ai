### flask - logger
- **概述：**
>       
>
>
>

- **logger使用：**
>       在/etc/supervisord.conf中配置日志的输出路径
>           stdout_logfile=/home/admin/workspace/flask/log/secDev.log                             
>           stderr_logfile=/home/admin/workspace/flask/log/secDev.err
>       然后在应用程序里执行下面的代码
>           from flask import current_app
>           current_app.logger.debug('debug')
>
>       或者配置在指定文件中：
>           https://segmentfault.com/q/1010000017196586/
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

- **待续：**
>       参考：http://www.techsite.cn/?p=12731
>             https://segmentfault.com/q/1010000017196586/
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
