## linux-shell - awk
- **概述：**
>
>
>
>
>
>
>

- **awk中对每一行进行正则匹配：**
>       awk '/^.*tcp.*$/ {sum[$6]++} END {for(i in sum) print i, sum[i]}'
>
>       1、过滤出字符中有 start worker 的行
>           awk '/^.*start worker.*$/ {print $0}' /usr/local/nginx/logs/error.log
>       2、以2019\/10\/20 10:59 开头的行
>           awk '/^2019\/10\/20 10:59/ {print $0}' /usr/local/nginx/logs/error.log
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

- **待续：**
>       参考：
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
