#coding=utf-8
import os
import time
import logging
import requests
from optparse import OptionParser
from apscheduler.schedulers.blocking import BlockingScheduler
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from srs_health_check_config import *
import subprocess

logging.basicConfig(level=log_level,
                format='[%(levelname)s] [%(asctime)s] [%(filename)s:%(lineno)d] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename= os.path.join(log_path, 'srs_health_check.log'),
                filemode='a+')
log = logging.getLogger()
logging.getLogger("requests").setLevel(logging.ERROR)
logging.getLogger("apscheduler").setLevel(logging.ERROR)

def notify_nginx_reload(notify_url):
    log.debug("notify nginx reload")
    pres = subprocess.Popen(check_except_nginx_reload, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    restatus, errorstatus = pres.communicate()
    if errorstatus:
        log.error("nginx reload error {0}".format(errorstatus))
    """
    res = None
    except_times = 0
    while except_times < int(check_except_update_times):
        try:
            res = requests.get(url=notify_url, timeout=check_except_update_timeout)
        except Exception as e:
            log.error("nginx reload error {0} {1}".format(notify_url, e))
            except_times += 1
        else:
            if int(res.status_code)/100 != 2:
                log.error("request error {0} {1}".format(notify_url, res.status_code))
                except_times += 1
            else:
                return True
    """

def health_check():
    good_addrs = list()
    try:
        if not os.path.exists(check_list_source_path):
            log.error("!!!!!!!!!!!!!!!! file {0} not exists".format(check_list_source_path))
            return
        with open(check_list_source_path, 'rb') as f:
            total_check = 0
            for line in f.xreadlines():
                if line:
                    line = line.strip()
                    if len(line.split(':')) != 2:
                        log.error("addr format error {0}".format(line))
                        continue
                    total_check += 1
                    log.debug("start check add {0}".format(line))
                    tmp_utl = 'http://{0}{1}'.format(line,health_api_url)
                    res = None
                    try:
                        res = requests.get(url=tmp_utl, timeout=int(health_api_url_timeout))
                    except Exception as e:
                        log.error("{0} get error {1}".format(line, e))
                    else:
                        if int(res.status_code) >= 200 and int(res.status_code) < 300:
                            good_addrs.append(line)
                            log.debug("addr {0} good".format(line))
            log.info("total check {0}".format(total_check))

        flag = False
        if not os.path.exists(check_list_result_path):
            with open(check_list_result_path, 'w') as f:
                pass

        old_check_list_count = 0
        with open(check_list_result_path, 'rb') as f:
            for line in f.xreadlines():
                if line:
                    old_check_list_count += 1
                    line = line.strip()
                    if line not in good_addrs:
                        flag = True
                        break
        if old_check_list_count != len(good_addrs):
            flag = True

        if flag:
            with open(check_list_result_path, 'wb') as f:
                for line in good_addrs:
                    line_list = line.split(':')
                    port_str = ''
                    if len(line_list) == 2:
                        if line_list[1] == '1985':
                            port_str = '1935'
                        elif line_list[1] == '1986':
                            port_str = '1936'
                        if port_str:
                            f.write("{0}:{1}\n".format(line_list[0], port_str))
            notify_nginx_reload(check_except_update_url)
        else:
            log.info("health check good, no addr check error")
    except Exception as e:
        log.error("check error {0}".format(e))

check_addrs_results_list = list()
def cross_speed_check():
    try:
        global check_addrs_results_list
        if not os.path.exists(cross_speed_list_source_path):
            log.error("file not exists {0}".format(cross_speed_list_source_path))
            return False
        log.debug("start cross speed check")
        check_result_map = {}
        check_addrs_list = list()
        with open(cross_speed_list_source_path, 'rb') as f:
            for line in f.xreadlines():
                if line:
                    line = line.strip()
                    log.debug("start cross speed check {0}".format(line))
                    check_addrs_list.append(line)
                    req_url = 'http://{0}{1}'.format(line,speed_check_api_url)
                    begin = time.time()
                    res = None
                    try:
                        res = requests.get(url=req_url, timeout=int(speed_check_api_timeout))
                    except Exception as e:
                        log.error("check {0} cross speed error {1}".format(req_url, e))
                    else:
                        cost_time = time.time() - begin
                        speed_value = float(len(res.content)/cost_time)
                        check_result_map[line] = speed_value
                        log.debug("cross speed check {0} {1}".format(line, speed_value))

        check_addrs_results_list.append(check_result_map)
        while len(check_addrs_results_list) > speed_check_times_decide:
            check_addrs_results_list.pop(0)
        flag = False
        if len(check_addrs_results_list) == speed_check_times_decide:
            for j in xrange(len(check_addrs_list) - 1):
                check_result_count = 0
                for i in xrange(len(check_addrs_results_list)):
                    if check_addrs_results_list[i].has_key(check_addrs_list[j]) and check_addrs_results_list[i].has_key(check_addrs_list[j+1]):
                        if check_addrs_results_list[i][check_addrs_list[j+1]] - check_addrs_results_list[i][check_addrs_list[j]] > float(speed_check_diff_limit):
                            check_result_count += 1
                if check_result_count == speed_check_times_decide:
                    check_addrs_list[j], check_addrs_list[j+1] = check_addrs_list[j+1], check_addrs_list[j]
                    flag = True
                    log.info("cross speed addr change {0} {1}".format(check_addrs_list[j], check_addrs_list[j+1]))
            if flag:
                tmp_check_list = list()
                if not os.path.exists(cross_speed_list_result_path):
                    log.error("file not exists {0}".format(cross_speed_list_result_path))
                    return False
                with open(cross_speed_list_result_path, 'rb') as f:
                    for i in f.xreadlines():
                        if i:
                            tmp_check_list.append(i.strip())
                inner_flag = False
                #判断之前是否已经通知过
                if tmp_check_list != check_addrs_list:
                    inner_flag = True
                if inner_flag:
                    with open(cross_speed_list_result_path, 'wb') as f:
                        for i in xrange(len(check_addrs_list)):
                            f.write("{0}\n".format(check_addrs_list[i]))
                    notify_nginx_reload(speed_check_except_update_url)
    except Exception as e:
        log.error("cross_speed_check error {0}".format(e))

def daemon(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    try:
        pid = os.fork()
        if pid > 0:
            # this parent, then exit
            sys.exit(0)
    except Exception as e:
        sys.stderr.write("fork 1 failed, {0}\n".format(e))
        raise

    # this is the first forked child process
    # separate from parent's environment
    os.chdir('/')
    os.setsid()
    os.umask(0)

    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except Exception as e:
        sys.stderr.write("fork 2 failed, {0}\n".format(e))
        raise

    # this is the second forded process
    # set fd
    sys.stdout.flush()
    sys.stderr.flush()
    stdin = file(stdin, 'r')
    stdout = file(stdout, 'a+')
    stderr = file(stderr, 'a+', 0)
    os.dup2(stdin.fileno(), sys.stdin.fileno())
    os.dup2(stdout.fileno(), sys.stdout.fileno())
    os.dup2(stderr.fileno(), sys.stderr.fileno())

def main():
    while True:
        try:
            sched = BlockingScheduler()
            sched.add_job(health_check, 'interval', seconds=health_check_frep)
            sched.add_job(cross_speed_check, 'interval', seconds=cross_speed_check_frep)
            sched.start()
        except Exception as e:
            log.error("{0}".format(e))
            time.sleep(0.1)

if __name__ == "__main__":
    is_daemon = False
    opt = OptionParser()
    opt.add_option('-d',
                    action="store_true",
                    dest="is_daemon",
                    default=False,
                    help="run the scripts daemon")
    opts, args = opt.parse_args()
    is_daemon = opts.is_daemon
    if is_daemon:
        daemon()
    main()
