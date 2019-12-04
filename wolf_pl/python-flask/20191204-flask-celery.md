### flask - celery
- **概述：**
>
>
>
>
>

- **celery启动后台流程：**
>       1、后台路由处理
>           async_send_email.delay(msg)
>           async_send_email.apply_async(args=[msg], countdown=60)
>       2、后台异步任务
>           @celery.task(bind=True)
>           def long_task(self):
>               self.update_state(state=u'处理中', meta={'current': i, 'total': total})
>       3、启动后台任务
>           @app.route('/longtask')
>           def longtask():
>               # 开启异步任务
>               task = long_task.apply_async()
>       4、获取任务状态信息的路由
>           @app.route('/status/<task_id>')
>           def taskstatus(task_id):
>               # 获取异步任务结果
>               task = long_task.AsyncResult(task_id)
>

- **celery启动命令：**
>       celery -A proj.task worker --loglevel=info
>       celery -A tasks worker --loglevel=info
>           -A 是指对应的应用程序, 其参数是项目中 Celery实例的位置，也即 celery_app = Celery()的位置
>           worker 是指这里要启动其中的worker，此时，就启动了一个worker
>
>       注意：
>           启动目录不对的话，会有问题
>

- **连接redis：**
>       redis://:password@hostname:port/db_number
>       redis://localhost:6379/0
>       URL 的所有配置都可以自定义配置的，默认使用的是 localhost 的 6379 端口中 0 数据库
>
>
>
>
>
>
>
>

- **待续：**
>       参考：https://www.cnblogs.com/cwp-bg/p/10575688.html
>           https://segmentfault.com/a/1190000008022050     分布式队列神器 Celery
>           https://blog.51cto.com/steed/2292346?source=dra     Celery 全面学习笔记
>           https://github.com/keejo125/flask_celery_redis_demo     flask_celery_redis demo
>
>           http://www.pythondoc.com/flask-celery/first.html#id6
>           https://www.jianshu.com/p/d55075240968
>           https://github.com/happy-python/flask_celery    Flask + Celery 实战(同上，异步发送邮件，显示进度更新和结果)
>
>
>           https://github.com/paicha/gxgk-wechat-server    校园微信公众号，使用 Python、Flask、Redis、MySQL、Celery
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
