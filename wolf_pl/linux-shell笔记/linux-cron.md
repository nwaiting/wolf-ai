### linux-shell - crontab
- **概述：**
>       格式：分 时 日 月 星期 要运行的命令
>       例如：30 21 * * * /apps/bin/cleanup.sh
>            表示每晚的21:30运行/apps/bin目录下的cleanup.sh
>
>           */1 * * * * /apps/bin/cleanup.sh
>           每一分钟执行一次
>
>           * * * * * sleep 1;/apps/bin/cleanup.sh
>           每一秒执行一次
>
>           45 4 1,10,22 * * /apps/bin/cleanup.sh
>           每月1、10、22日
>
>           0 */2 * * * /apps/bin/cleanup.sh
>           每两个小时
>
>           0 23-7/2，8 * * * /apps/bin/cleanup.sh
>           晚上11点到早上8点之间每两个小时
>
>
>
>
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
