#coding=utf-8
#日志目录
log_path = '/home/logs/newlive'
"""
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0
"""
log_level = 10

#检测地址源 目录
check_list_source_path = '/usr/local/newlive/source_list.data'

#检测后存放目录
check_list_result_path = '/usr/local/newlive/result_list.data'

#异常通知 ng重启
check_except_nginx_reload = '/usr/local/nginx/sbin/nginx -c /usr/local/newlive/conf/nginx/nginx-schedule.conf -s reload'
check_except_update_url = ''
#通知nginx测速结果
speed_check_except_update_url = ''
#失败后重试次数
check_except_update_times = 3
#通知nginx超时时间
check_except_update_timeout = 2

#srs的健康检测API
health_api_url = '/api/v1/vhosts/?callback=JSON_CALLBACK'
health_api_url_timeout = 2

#srs的健康检测频率
health_check_frep = 3

############################################
#机房测速
############################################
#机房检测频率
cross_speed_check_frep = 3

#需要检测的机房列表
cross_speed_list_source_path = ''
cross_speed_list_result_path = ''

#机房检测的下载地址
speed_check_api_url = ''
speed_check_api_timeout = 2

#多次检测确定结果
speed_check_times_decide = 3
speed_check_diff_limit = 1000
