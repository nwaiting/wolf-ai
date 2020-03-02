### celery 相关
- **概述：**
>
>
>
>
>
>
>

- **Celery介绍：**
>       Celery的架构由三部分组成：
>           1、消息中间件（message broker）
>               CELERY_BROKER_URL 配置
>               这个broker有几个方案可供选择：RabbitMQ（消息队列），Redis（缓存数据库），数据库（不推荐），等等，对于brokers，官方推荐是rabbitmq和redis
>           2、任务执行单元（worker）
>
>           3、任务执行结果存储（task result store）组成
>               CELERY_RESULT_BACKEND 配置选项
>               至于backend，就是数据库，为了简单可以都使用redis
>

- **使用Celery：**
>       使用celery包含三个方面：
>           1、定义任务函数
>           2、运行celery服务
>           3、客户应用程序的调用
>
>       启动Celery：
>           在proj的同一级目录执行celery命令
>           celery -A proj worker -l info
>
>

- **Celery配置定时任务：**
>       Scheduler(定时任务，周期性任务)
>       在celery中执行定时任务非常简单，只需要设置celery对象的CELERYBEAT_SCHEDULE属性即可
>       CELERYBEAT_SCHEDULE     配置项
>       CELERY_TIMEZONE = 'Asia/Shanghai'
>       注意配置文件需要指定时区，一旦使用了scheduler，启动celery需要加上-B参数
>       celery -A proj worker -B -l info
>
>

- **常用配置：**
>       CELERY_ROUTES
>           通过CELERY_ROUTES来为每一个task指定队列
>           如果有任务到达时，通过任务的名字来让指定的worker来处理
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


- **待续：**
>       参考：http://liyangliang.me/posts/2015/11/using-celery-with-flask/?utm_source=tuicool&utm_medium=referral
>           https://www.cnblogs.com/daqingzi/p/9641591.html     Celery详解
>           https://www.jianshu.com/p/4d0bbdbc6ade      CELERY CELERY_QUEUES和CELERY_ROUTS的用法
>           https://blog.csdn.net/qq_24861509/article/details/83863782
>           https://www.cnblogs.com/cwp-bg/p/8759638.html   python之celery使用详解一
>
>           https://blog.csdn.net/qq_33339479/article/details/80961182      celery源码分析-Task的初始化与发送任务
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
