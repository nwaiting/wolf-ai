## nginx - nginx日志回滚系统配置
- **概述：**
>       Linux自带的logrotate来管理日志：
>       [hello ~]$ cat /etc/logrotate.d/nginx
>           /home/logs/nginx/*.log {
>               notifempty
>               copytruncate
>               dateext
>               daily
>               rotate 10
>               compress
>               missingok
>           }
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
