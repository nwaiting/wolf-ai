## zabbix - base
- **概述：**
>       添加自定义数据流程：
>           1、有一个默认的配置文件，/etc/zabbix/zabbix_agentd.conf，
>               配置文件里面有 Include 字段，引入其他的conf文件，如：
>               Include=/etc/zabbix/zabbix_agentd.d/
>           2、比如自定义的监控的conf文件，/etc/zabbix/zabbix_agentd.d/userparameter_apache.conf
>               内部定义 UserParameter 监控字段，如：
>               UserParameter=httpd.port.discovery,/usr/bin/python2.6 /opt/zabbix/lldscripts/httpd_low_level_discovery.py
>           3、httpd_low_level_discovery.py文件内部打印输出字符串，如：
>               print(json.dumps({'data':ports}))
>

- **zabbix_sender主动上报：**
>       zabbix_sender命令支持主动上报数据，web服务端添加对应机器和采集器即可
>       客户端主动调用上传的命令：
>           os.system("%s -z %s -s %s -k %s -o %s -vv" % (zabbix_sender,zabbix_server,my_ip,'liuyan',mysql_data))
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
