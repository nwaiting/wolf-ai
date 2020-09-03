import os
import json
import requests
from requests.auth import HTTPProxyAuth
from lxml import etree
import time
import datetime
import random
import threading
from queue import Queue
import logging
import pymysql
from DBUtils.PersistentDB import PersistentDB

log_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "{}.log".format(os.path.basename(__file__)))
logging.basicConfig(level=logging.INFO,
    filename=log_file,
    format=('[%(levelname)s %(asctime)s.%(msecs)03d] [%(process)d:%(threadName)s:%(funcName)s:%(lineno)d] %(message)s'),
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
    ]
base_url = 'https://github.com/'


def write_file(contents):
    with open('{}.html'.format(datetime.datetime.now().strftime("%y_%m_%d_%H_%M_%S")), 'wb') as f:
        f.write(contents.encode('utf-8'))


def to_int(s, default=0):
    if isinstance(s, int):
        return s

    s = s.strip('\r\n ').replace(',', '')
    try:
        return int(s)
    except:
        return default


def clean_str(s):
    if isinstance(s, list) and len(s) > 0:
        s = s[0]
    if isinstance(s, str):
        s = s.strip('\r\n ').replace(' ', '')
        return s
    return s


def clean_str_cr(s):
    if isinstance(s, list) and len(s) > 0:
        s = s[0]
    if isinstance(s, str):
        lines = []
        for line in s.split('\n'):
            line = line.strip('\r\n ')
            if line:
                lines.append(line)
        return ','.join(lines)
    return s


def get_headers(referer):
    headers = {
        "Host": "github.com",
        "If-None-Match": 'W/"e13fd2a7072437a5541964a18151f4d7"',
        "Referer": "{}".format(referer),
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "{}".format(random.choice(user_agent_list))
    }
    return headers


class InnerObj(object):
    def __init__(self, status_code=400, msg='err'):
        self.status_code = status_code
        self.msg = msg
        self.text = ''


class ProxyHandler(object):
    def __init__(self):
        self._ip_list = []
        self._current_proxy = self.get_valid_proxy()

    def get_valid_proxy(self):
        ""
        proxies_list = ['', None]
        select_proxy = random.choice(proxies_list)
        if select_proxy:
            self._current_proxy = {
                'http': "http://{}".format(select_proxy),
                'https': "https://{}".format(select_proxy)
            }
        else:
            self._current_proxy = None
        return self._current_proxy

        """
        if not self._ip_list:
            proxy_list_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "proxies")
            with open(proxy_list_file, 'rb') as f:
                for line in f.readlines():
                    line = line.decode('utf-8').strip('\r\n ')
                    if line:
                        self._ip_list.append(line)
        while True:
            ip = random.choice(self._ip_list)
            proxies = {
                'http': ip,
                'https': ip
            }
            url = 'https://www.baidu.com/'
            headers = get_headers(url)
            try:
                res = requests.get(url, headers=headers, proxies=proxies, timeout=3)
                if res.status_code == 200:
                    return proxies
            except Exception as e:
                time.sleep(0.2)
        """

    def change_proxy(self):
        self._current_proxy = self.get_valid_proxy()
        logger.info("current proxy {}".format(self._current_proxy))

    def get(self, url, params=None, headers=None):
        for _ in range(3):
            try:
                res = requests.get(url, params=params, headers=headers, proxies=self._current_proxy, timeout=5)
                if int(res.status_code / 100) == 4:
                    logger.info("{} start change proxy".format(url))
                    self.change_proxy()
                    time.sleep(0.2)
                    continue
                return res
            except Exception as e:
                logger.error("{} {}:{} {}".format(_, url, e, params))
                self.change_proxy()
                time.sleep(0.2)
        return InnerObj()


class SqlModel(object):
    def __init__(self, dbinfo):
        self._dbinfo = dbinfo if dbinfo else {}
        self._pool = None
        self._conn = None

    @property
    def conn(self):
        if not self._pool:
            self._pool = PersistentDB(
                creator=pymysql,
                maxusage=None,
                ping=0,
                closeable=False,
                threadlocal=None,
                host=self._dbinfo.get('HOST', '127.0.0.1'),
                port=self._dbinfo.get('PORT', 3306),
                user=self._dbinfo.get('USER', 'test'),
                password=self._dbinfo.get('PASSWORD', 'test'),
                database=self._dbinfo.get('DB', 'github'),
                charset='utf8mb4'
            )
        for _ in range(3):
            try:
                return self._pool.connection()
            except Exception as e:
                logger.error("SqlModel {}".format(e))
                time.sleep(1)
        return None

    def save_basic_info(self, datas):
        with self.conn as conn, conn.cursor() as cur:
            sql = "insert into tb_basic_info(repo_id,repo_name,commit_count,branch_count,package_count,release_count,contributors_count," \
                  "watch_count,star_count,fork_count,issue_count,pull_request_count,tags_count,license,topic,languages,link,get_ts) " \
                  "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update get_ts=values(get_ts)"
            try:
                cur.executemany(sql, datas)
            except Exception as e:
                logger.error("{} {}".format("save_basic_info", e))

    def save_release_version(self, datas):
        with self.conn as conn, conn.cursor() as cur:
            sql = "insert into tb_release_version(repo_id,repo_name,version_name,version_id,release_time,contributors," \
                  "link,release_documents,source_link,tag_id,verified,get_ts) " \
                  "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update get_ts=values(get_ts)"
            try:
                cur.executemany(sql, datas)
            except Exception as e:
                logger.error("{} {}".format("save_release_version", e))

    def save_commits(self, datas):
        with self.conn as conn, conn.cursor() as cur:
            sql = "insert into tb_commits(repo_id,repo_name,tag_id,commit_id,commitor,author," \
                  "commit_time,link,checkstatus,verified,commit_text,get_ts) " \
                  "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update get_ts=values(get_ts)"
            try:
                cur.executemany(sql, datas)
            except Exception as e:
                logger.error("{} {}".format("save_commits", e))

    def save_issues(self, datas):
        with self.conn as conn, conn.cursor() as cur:
            sql = "insert into tb_issues(repo_id,repo_name,issue_id,issue_link,issue_title,issue_label," \
                  "issue_project,issue_milestones,issue_linked_pull_request,open_time,participants,commitors," \
                  "assigners,assignee,issue_network_links,issue_text,get_ts) " \
                  "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update get_ts=values(get_ts)"
            try:
                cur.executemany(sql, datas)
            except Exception as e:
                logger.error("{} {}".format("save_issues", e))

    def save_pull_requests(self, datas):
        with self.conn as conn, conn.cursor() as cur:
            sql = "insert into tb_pull_requests(repo_id,repo_name,pull_request_id,pull_request_link,pull_request_title," \
                  "pull_request_label,pull_request_project,pull_request_milestones,linked_issue,open_time,participants," \
                  "commitors,assigners,assignee,get_ts) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update get_ts=values(get_ts)"
            try:
                cur.executemany(sql, datas)
            except Exception as e:
                logger.error("{} {}".format("save_pull_requests", e))


class SpiderHandleBase(object):
    def __init__(self, repo_id, repo_name):
        self._repo_id = repo_id
        self._repo_name = repo_name
        self._except_try_times = 3
        self._max_sleep_value = 5
        self._request_domain_base = 'https://github.com'
        self._proxy = ProxyHandler()
        self._sql_model = SqlModel(None)

    def maybe_sleep_for_while(self):
        time.sleep(random.uniform(0, self._max_sleep_value))

    def get(self, url, params=None, headers=None):
        return self._proxy.get(url, params=params, headers=headers)

    def save_db(self):
        pass


class PullRequestHandle(SpiderHandleBase):
    def __init__(self, pull_url_base, repo_id, repo_name):
        self._pull_url_base = pull_url_base
        super(PullRequestHandle, self).__init__(repo_id, repo_name)

    def get_page_details(self, url):
        result = {}
        res = None
        try:
            url = "{}{}".format(self._request_domain_base, url)
            logger.info("detail {}".format(url))
            headers = get_headers(self._pull_url_base)
            res = self.get(url, headers=headers)
            # res = requests.get(url, headers=headers)
        except Exception as e:
            logger.error("get_page_detail {} err {}".format(url, e))
            return result
        finally:
            self.maybe_sleep_for_while()

        html = etree.HTML(res.text)
        if not html:
            return result
        reviewers = html.xpath('//div[@id="partial-discussion-sidebar"]//form[@aria-label="Select reviewers"]/span/p/span//span[@class="css-truncate-target"]/text()')
        result["reviewers"] = ','.join(reviewers)
        assignees = html.xpath('//div[@id="partial-discussion-sidebar"]//form[@aria-label="Select assignees"]/span/text()')
        result["assignees"] = ','.join(assignees) if assignees else ''
        labels = html.xpath('//div[@id="partial-discussion-sidebar"]//div[@class="labels css-truncate js-issue-labels"]/a/span/text()')
        result["labels"] = ','.join([it.strip('\r\n ') for it in labels])
        projects = html.xpath('//div[@id="partial-discussion-sidebar"]//form[@aria-label="Select projects"]/span/div/div[last()]/div[1]/div/@aria-label')
        result["projects"] = projects[0] if projects else ''
        milestone = html.xpath('//div[@id="partial-discussion-sidebar"]//form[@aria-label="Select milestones"]/text()')
        new_milestone = []
        for it in milestone:
            it_str = it.strip('\r\n ')
            if it_str:
                new_milestone.append(it_str)
        result["milestone"] = ','.join(new_milestone)
        linked_issues = html.xpath('//div[@id="partial-discussion-sidebar"]//form[@aria-label="Link issues"]/p/text()')
        result["linked_issues"] = ','.join([it.strip('\r\n ') for it in linked_issues])
        participants = html.xpath('//div[@id="partial-discussion-sidebar"]/div[last()]/div/div[last()]/a/img/@alt')
        new_participants = []
        for it in participants:
            it_str = it.strip('\r\n ')
            if it_str:
                if it_str.startswith('@'):
                    it_str = it_str[1:]
                new_participants.append(it_str)
        result["participants"] = ','.join(new_participants)
        return result

    def get_pages(self):
        for page_type in ('open', 'closed'):
            for i in range(1, 1000):
                results = []
                url = '{}/pulls'.format(self._pull_url_base)
                headers = get_headers(self._pull_url_base)
                headers["If-None-Match"] = 'W/"cab2ea7c28cbb6326fa6a335326c1d29"'

                params = {
                    "page": "{}".format(i),
                    "q": "is:pr is:{}".format(page_type)
                }

                res = None
                try:
                    logger.info("start {} {}".format(url, params))
                    res = self.get(url, params=params, headers=headers)
                    # res = requests.get(url, params=params, headers=headers)
                    if res.status_code != 200:
                        logger.error("{} status {}".format(url, res.status_code))
                        break
                except Exception as e:
                    logger.error("{} {} err {}".format(self._except_try_times, url, e))
                    if self._except_try_times > 0:
                        self._except_try_times -= 1
                        continue
                    else:
                        break
                finally:
                    self.maybe_sleep_for_while()

                html = etree.HTML(res.text)
                for item in html.xpath('//div[@class="js-navigation-container js-active-navigation-container"]/div'):
                    pull_text = item.xpath('.//div[@class="flex-auto min-width-0 p-2 pr-3 pr-md-2"]/a/text()')
                    pull_text = pull_text[0] if pull_text else ''
                    pull_url = item.xpath('.//div[@class="flex-auto min-width-0 p-2 pr-3 pr-md-2"]/a/@href')
                    pull_url = pull_url[0] if pull_url else ''
                    page_detail = self.get_page_details(pull_url)
                    pull_id = to_int(os.path.basename(pull_url))
                    pull_labels = item.xpath('string(.//div[@class="flex-auto min-width-0 p-2 pr-3 pr-md-2"]/span[2])')
                    pull_labels = pull_labels[0] if pull_labels else ''
                    pull_opened_by = item.xpath('.//div[@class="flex-auto min-width-0 p-2 pr-3 pr-md-2"]/div/span[1]/text()')
                    pull_opened_by = pull_opened_by[0] if pull_opened_by else ''
                    pull_opened_creater = item.xpath('.//div[@class="flex-auto min-width-0 p-2 pr-3 pr-md-2"]/div/span[1]/a/text()')
                    pull_opened_creater = pull_opened_creater[0] if pull_opened_creater else ''
                    pull_time = item.xpath('.//div[@class="flex-auto min-width-0 p-2 pr-3 pr-md-2"]/div/span[1]/relative-time/@datetime')
                    pull_time = pull_time[0] if pull_time else ''
                    pull_changes_requested = item.xpath('.//div[@class="flex-auto min-width-0 p-2 pr-3 pr-md-2"]/div/span[2]/a/text()')
                    pull_changes_requested = pull_changes_requested[0] if pull_changes_requested else ''

                    results.append((self._repo_id,self._repo_name,pull_id,pull_url,pull_text,
                                    page_detail.get('labels', ''),page_detail.get('projects', ''),
                                    page_detail.get('milestone', ''),page_detail.get('linked_issues', ''),
                                    pull_time,page_detail.get('participants', ''),'',
                                    page_detail.get('assignees', ''),page_detail.get('assignees', ''),int(time.time())))

                if results:
                    self._sql_model.save_pull_requests(results)
                    if len(results) <= 5:
                        break
                else:
                    break

    def run(self):
        self.get_pages()


class IssueHandle(SpiderHandleBase):
    def __init__(self, issue_url_base, repo_id, repo_name):
        self._issue_url_base = issue_url_base
        super(IssueHandle, self).__init__(repo_id, repo_name)

    def get_page_detail(self, url):
        result = {}
        res = None
        try:
            url = "{}{}".format(self._request_domain_base, url)
            logger.info("detail {}".format(url))
            headers = get_headers(self._issue_url_base)
            res = self.get(url, headers=headers)
            # res = requests.get(url, headers=headers)
        except Exception as e:
            logger.error("get_page_detail {} err {}".format(url, e))
            return result
        finally:
            self.maybe_sleep_for_while()

        html = etree.HTML(res.text)
        if not html:
            return result
        item_assignees = html.xpath('//div[@id="partial-discussion-sidebar"]//form[@aria-label="Select assignees"]/span/p/span/a[last()]/span/text()')
        result["item_assignees"] = ','.join(item_assignees)
        item_labels = html.xpath('//div[@id="partial-discussion-sidebar"]//div[@class="labels css-truncate js-issue-labels"]/a/span/text()')
        result["item_labels"] = ','.join(item_labels)
        item_projects = html.xpath('//div[@id="partial-discussion-sidebar"]//form[@aria-label="Select projects"]/span/text()')
        result["item_projects"] = item_projects[0] if item_projects else ''
        item_milestones = html.xpath('//div[@id="partial-discussion-sidebar"]//form[@aria-label="Select milestones"]/text()')
        if item_milestones:
            tmp_str = ''
            for it in item_milestones:
                if it.strip('\r\n '):
                    tmp_str += it.strip('\r\n ')
            result["item_milestones"] = tmp_str
        item_linked_pull_requests = html.xpath('string(//div[@id="partial-discussion-sidebar"]//form[@aria-label="Link issues"])')
        if item_linked_pull_requests:
            result["item_linked_pull_requests"] = clean_str_cr(item_linked_pull_requests)
        item_notifications = html.xpath('//div[@id="partial-discussion-sidebar"]/div[last()-1]/div/p/text()')
        result["item_notifications"] = item_notifications[0] if item_notifications else ''

        item_participants = []
        for item in html.xpath('//div[@id="partial-discussion-sidebar"]/div[last()]/div/div[last()]/a/img/@alt'):
            item_str = item.strip('\r\n ')
            if item_str:
                if item_str.startswith('@'):
                    item_str = item_str[1:]
                item_participants.append(item_str)
        result["item_participants"] = ','.join(item_participants) if item_participants else ''
        issue_network_links = []
        for item in html.xpath('//div[@class="TimelineItem js-targetable-element"]'):
            issue_network_links.append(item.xpath('string(./div[2])'))
        result["issue_network_links"] = json.dumps(issue_network_links)
        result["issue_text"] = html.xpath('string(//div[@class="edit-comment-hide"]/task-lists/table/tbody/tr/td/ul[1])')
        return result

    def get_pages(self):
        for page_type in ('open', 'closed'):
            for i in range(1, 1000):
                results = []
                url = '{}/issues'.format(self._issue_url_base)
                headers = get_headers(self._issue_url_base)
                headers["If-None-Match"] = 'W/"cab2ea7c28cbb6326fa6a335326c1d29"'

                params = {
                    "page": "{}".format(i),
                    "q": "is:issue is:{}".format(page_type)
                }

                res = None
                try:
                    logger.info("{} {}".format(url, params))
                    res = self.get(url, params=params, headers=headers)
                    # res = requests.get(url, params=params, headers=headers)
                    if res.status_code != 200:
                        logger.error("{} status {}".format(url, res.status_code))
                        break
                except Exception as e:
                    logger.error("{} {} err {}".format(self._except_try_times, url, e))
                    if self._except_try_times > 0:
                        self._except_try_times -= 1
                        continue
                    else:
                        continue
                finally:
                    self.maybe_sleep_for_while()

                if res.status_code != 200:
                    logger.error("{} {} {}".format(url, params, res.status_code))
                    break

                html = etree.HTML(res.text)
                for item in html.xpath('//div[@class="js-navigation-container js-active-navigation-container"]/div'):
                    issuse_status = item.xpath('./div/div[1]/span/@aria-label')
                    issuse_status = issuse_status[0] if issuse_status else ''
                    issuse_text = item.xpath('./div/div[2]/a/text()')
                    issuse_text = issuse_text[0] if issuse_text else ''
                    issuse_url = item.xpath('./div/div[2]/a/@href')
                    issuse_url = issuse_url[0] if issuse_url else ''
                    issuse_id = os.path.basename(issuse_url)
                    res_details = self.get_page_detail(issuse_url)
                    issuse_labels = item.xpath('./div/div[2]/span/a/text()')
                    issuse_labels = issuse_labels[0] if issuse_labels else ''
                    issuse_time = item.xpath('./div/div[2]/div/span/relative-time/@datetime')
                    issuse_time = issuse_time[0] if issuse_time else ''
                    issuse_open_author = item.xpath('./div/div[2]/div/span/a/text()')
                    issuse_open_author = issuse_open_author[0] if issuse_open_author else ''

                    results.append((self._repo_id,self._repo_name,issuse_id,issuse_url,issuse_text,issuse_labels,res_details.get('item_projects', ''),
                                    res_details.get('item_milestones', ''),res_details.get('item_linked_pull_requests', '')
                                    ,issuse_time,res_details.get('item_participants', ''),issuse_open_author,
                                    res_details.get('item_assignees', ''),res_details.get('item_assignees', ''),
                                    res_details.get('issue_network_links', ''),res_details.get('issue_text', ''),
                                    int(time.time())))
                if results:
                    self._sql_model.save_issues(results)
                    if len(results) <= 5:
                        break
                else:
                    break

    def run(self):
        self.get_pages()


class CommiterHandle(SpiderHandleBase):
    def __init__(self, versions, commit_url_base, repo_id, repo_name):
        self._commit_url_base = commit_url_base
        self._versions = versions
        self._next_page_id = None
        self._next_page_count = 0

        super(CommiterHandle, self).__init__(repo_id, repo_name)

    def get_pages(self):
        for version in self._versions:
            while True:
                results = []
                params = None
                if self._next_page_count:
                    url = '{}/commits/{}'.format(self._commit_url_base, version)
                    params = {
                        "after": "{} {}".format(self._next_page_id, self._next_page_count),
                        "branch": "{}".format(version)
                    }
                else:
                    url = '{}/commits/{}'.format(self._commit_url_base, version)

                headers = get_headers(self._commit_url_base)
                headers["Referer"] = "{}".format(self._commit_url_base)

                res = ''
                try:
                    logger.info("start {} {}".format(url, params))
                    res = self.get(url, params=params, headers=headers)
                except Exception as e:
                    logger.error("{} {} {}".format(self.__class__, url, e))
                    break
                finally:
                    self.maybe_sleep_for_while()

                if res.status_code == 200:
                    html = etree.HTML(res.text)
                    li_items = html.xpath('//div[@class="TimelineItem-body"]/ol/li')
                    index = 0
                    for li_item in li_items:
                        commit_text = li_item.xpath('./div[@class="flex-auto min-width-0"]/p/a/text()')
                        commit_text = ','.join(commit_text) if commit_text else ''
                        commit_url = li_item.xpath('./div[@class="flex-auto min-width-0"]/p/a/@href')
                        commit_url = commit_url[0] if commit_url else ''
                        commit_id = os.path.basename(commit_url)
                        if index == 0:
                            self._next_page_id = commit_id
                            index += 1
                        authors = li_item.xpath('.//div[@class="f6 text-gray min-width-0"]/a/text()')
                        commitor = ''
                        author = ''
                        if len(authors) == 2:
                            author = authors[0]
                            commitor = authors[1]
                        elif len(authors) == 1:
                            commitor = authors[0]
                        commit_time = li_item.xpath('.//div[@class="f6 text-gray min-width-0"]/relative-time/@datetime')
                        commit_time = commit_time[0] if commit_time else ''
                        link = li_item.xpath('./div[1]/p/a/@href')
                        link = link[0] if link else ''
                        checkstatus = li_item.xpath('./div[1]/div[last()]/div[last()]/details/summary/@class')
                        checkstatus = checkstatus[0] if checkstatus else 'None'
                        verified = li_item.xpath('./div[last()]/details/summary/text()')
                        verified = clean_str(verified) if verified else 'None'
                        results.append((self._repo_id,self._repo_name,version,commit_id,commitor,author,commit_time,link,
                                        checkstatus,verified,commit_text,int(time.time())))
                    self._next_page_count = len(li_items) - 1
                if results:
                    self._sql_model.save_commits(results)
                    if len(results) <= 5:
                        break
                else:
                    break

    def run(self):
        self.get_pages()


class GetRepo(threading.Thread):
    def __init__(self, repo_url_queue):
        self._repo_url_queue = repo_url_queue
        self._repo_url = None
        self._repo_id = None
        self._repo_name = None
        self._branch_versions = []

        self._sql_model = SqlModel(None)

        self._proxy = ProxyHandler()

        self._commiter_handle = None
        self._issue_handle = None
        self._pull_request_handle = None
        super(GetRepo, self).__init__()

    def get(self, url, params=None, headers=None):
        return self._proxy.get(url, params=params, headers=headers)

    def get_basic_info(self):
        results = []
        headers = get_headers(self._repo_url)
        res = ''
        try:
            logger.info("basic info {}".format(self._repo_url))
            res = self.get(self._repo_url, headers=headers)
            # res = requests.get(self._repo_url, headers=headers)
        except Exception as e:
            logger.error("{} msg {}".format(self._repo_url, e))
            return {}
        finally:
            time.sleep(random.randint(1, 5))

        if res.status_code != 200:
            logger.error("{} response status {}".format(self._repo_url, res.status_code))
            return results

        html = etree.HTML(res.text)
        if not html:
            return results
        repo_id = html.xpath('//meta[@name="octolytics-dimension-repository_id"]/@content')
        repo_id = repo_id[0] if repo_id else '0'
        self._repo_id = repo_id
        repo_name = self._repo_name = os.path.basename(self._repo_url)
        issue_count = html.xpath('//ul[@class="UnderlineNav-body list-style-none "]/li[2]/a/span[2]/@title')
        issue_count = to_int(issue_count[0] if issue_count else '0')
        pull_request_count = html.xpath('//ul[@class="UnderlineNav-body list-style-none "]/li[3]/a/span[2]/@title')
        pull_request_count = to_int(pull_request_count[0] if pull_request_count else '0')
        branches_count = html.xpath('//div[@class="file-navigation mb-3 d-flex flex-items-start"]/div[2]/a[1]/strong/text()')
        branches_count = to_int(branches_count[0] if branches_count else '0')
        tags_count = html.xpath('//div[@class="file-navigation mb-3 d-flex flex-items-start"]/div[2]/a[2]/strong/text()')
        tags_count = to_int(tags_count[0] if tags_count else '0')
        commit_count = html.xpath('//div[@class="flex-shrink-0"]/ul/li/a/span/strong/text()')
        commit_count = to_int(commit_count[0] if commit_count else '0')
        watch_count = html.xpath('//main[@id="js-repo-pjax-container"]/div[1]/div[1]/ul/li[last()-2]/a[last()]/@aria-label')
        watch_count = watch_count[0] if watch_count else '0'
        watch_count = to_int(watch_count.split()[0])

        star_count = html.xpath('//main[@id="js-repo-pjax-container"]/div[1]/div[1]/ul/li[last()-1]/a[last()]/@aria-label')
        star_count = star_count[0] if star_count else '0'
        star_count = to_int(star_count.split()[0])

        fork_count = html.xpath('//main[@id="js-repo-pjax-container"]/div[1]/div[1]/ul/li[last()]/a[last()]/@aria-label')
        fork_count = fork_count[0] if fork_count else '0'
        fork_count = to_int(fork_count.split()[0])

        topic = html.xpath('//div[@class="BorderGrid BorderGrid--spacious"]/div[1]/div/div//a[@data-octo-click="topic_click"]/text()')
        topic = ','.join([it.strip('\r\n ') for it in topic]) if topic else ''

        license = html.xpath('//div[@class="BorderGrid BorderGrid--spacious"]/div[1]/div/div[last()]/a/text()')
        new_license = ''
        if license:
            for it in license:
                if it.strip('\r\n '):
                    new_license += it.strip('\r\n ')
        license = new_license

        release_count = html.xpath('//div[@class="BorderGrid BorderGrid--spacious"]/div[2]/div/h2/a/span/text()')
        release_count = to_int(release_count[0] if release_count else 0)

        packages = html.xpath('//div[@class="BorderGrid BorderGrid--spacious"]/div[3]/div/div/text()')
        packages = to_int(packages[0] if packages else '')

        languages = []
        for language_item in html.xpath('//div[@class="BorderGrid BorderGrid--spacious"]/div[last()]/div/ul/li'):
            if language_item.xpath('./a/span[1]/text()'):
                languages.append({
                    language_item.xpath('./a/span[1]/text()')[0]: language_item.xpath('./a/span[2]/text()')[0]
                })
            if language_item.xpath('./span/span[1]/text()'):
                languages.append({
                    language_item.xpath('./span/span[1]/text()')[0]: language_item.xpath('./span/span[2]/text()')[0]
                })

        contributors = html.xpath('//div[@class="BorderGrid BorderGrid--spacious"]/div[5]/div/h2/a/span/text()')
        contributors = to_int(contributors[0] if contributors else '')
        results.append((repo_id, repo_name, commit_count, branches_count, packages, release_count, contributors,
                        watch_count, star_count, fork_count, issue_count, pull_request_count, tags_count,
                        license, topic, json.dumps(languages), self._repo_url, int(time.time())
                        ))
        return results

    def get_release_version(self):
        next_page_after = ''
        while True:
            results = []
            headers = get_headers(self._repo_url)
            url = "{}/releases".format(self._repo_url)
            params = {}
            if next_page_after:
                params = {
                    "after": "{}".format(next_page_after)
                }
            res = ''
            try:
                logger.info("start {} {}".format(url, params))
                res = self.get(url, headers=headers, params=params)
            except Exception as e:
                logger.error("{} msg {}".format(url, e))
                return {}
            finally:
                time.sleep(random.randint(1, 5))

            if res.status_code != 200:
                logger.error("{} response status {}".format(url, res.status_code))
                break

            html = etree.HTML(res.text)
            for item in html.xpath('//div[@class="release-entry"]'):
                version_id = item.xpath('./div/div[1]/ul/li[1]/a/@title')
                version_id = version_id[0] if version_id else ''
                tag_id = version_id
                if version_id:
                    next_page_after = version_id
                verified = item.xpath('./div/div[1]/ul/li[3]/details/summary/text()')
                verified = verified[0] if verified else 'NOT'
                link = item.xpath('./div/div[2]/div[1]/div/div/a/@href')
                link = link[0] if link else ''
                version_name = item.xpath('./div/div[2]/div[1]/div/div/a/text()')
                version_name = version_name[0] if version_name else ''
                if not version_name:
                    continue
                release_time = item.xpath('./div/div[2]/div[1]/p/relative-time/@datetime')
                release_time = release_time[0] if release_time else ''
                contributors = []
                contributors_title = item.xpath('./div/div[2]/div[2]/h2[last()]/text()')
                if contributors_title:
                    if contributors_title[0].find('Contributors') > 0:
                        contributors = item.xpath('./div/div[2]/div[2]/p[last()]/text()')
                contributors = json.dumps(contributors)
                documents = item.xpath('string(./div/div[2]/div[2])')
                documents = documents[0] if documents else ''
                source_link = item.xpath('./div/div[2]/details/div/div/div[1]/a/@href')
                source_link = source_link[0] if source_link else ''

                results.append((self._repo_id,self._repo_name,version_name,version_id,release_time,contributors,
                                link,documents,source_link,tag_id,verified,int(time.time())))

            if results:
                self._sql_model.save_release_version(results)
                if len(results) <= 3:
                    break
            else:
                break

    def get_all_versions(self):
        for i in range(1, 200):
            url = '{}/branches/all?page={}'.format(self._repo_url, i)
            headers = get_headers(self._repo_url)
            headers["Referer"] = "{}".format(self._repo_url)
            res = ''
            try:
                res = self.get(url, headers=headers)
                # res = requests.get(url, headers=headers)
            except Exception as e:
                logger.error("{} msg {}".format(url, e))
                break
            finally:
                time.sleep(random.randint(1, 5))

            if res.status_code != 200:
                logger.error("{} response status {}".format(url, res.status_code))
                break
            html = etree.HTML(res.text)
            for item in html.xpath('//div[@class="Box mb-3"]/ul/li'):
                branch_name = item.xpath('./branch-filter-item/div/a/text()')
                branch_name = branch_name[0] if branch_name else ''
                self._branch_versions.append(branch_name)

    def get_all_tags(self):
        next_page_after = ''
        results = []
        while True:
            headers = get_headers(self._repo_url)
            url = "{}/tags".format(self._repo_url)
            params = {}
            if next_page_after:
                params = {
                    "after": "{}".format(next_page_after)
                }
            res = ''
            try:
                logger.info("start {} {}".format(url, params))
                res = self.get(url, headers=headers, params=params)
            except Exception as e:
                logger.error("{} msg {}".format(url, e))
                return {}
            finally:
                time.sleep(random.randint(1, 5))

            if res.status_code != 200:
                logger.error("{} response status {}".format(url, res.status_code))
                break

            html = etree.HTML(res.text)
            current_len = 0
            for item in html.xpath('//div[@class="flex-auto min-width-0"]'):
                current_len += 1
                item_tag = item.xpath('./div/div[1]/h4/a/text()')
                if item_tag:
                    results.append(item_tag[0].strip('\r\n '))
                    next_page_after = item_tag[0].strip('\r\n ')
            if current_len <= 5:
                break
        return results

    def run(self):
        while not self._repo_url_queue.empty():
            self._repo_url = self._repo_url_queue.get()
            basic_infos = self.get_basic_info()
            self._sql_model.save_basic_info(basic_infos)

            self.get_release_version()

            tags = self.get_all_tags()
            self._commiter_handle = CommiterHandle(tags, self._repo_url, self._repo_id, self._repo_name)
            self._commiter_handle.run()

            self._issue_handle = IssueHandle(self._repo_url, self._repo_id, self._repo_name)
            self._issue_handle.run()

            self._pull_request_handle = PullRequestHandle(self._repo_url, self._repo_id, self._repo_name)
            self._pull_request_handle.run()


def get_tasks(input_queue):
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '300_topic_links.txt')
    with open(file_path, 'rb') as f:
        for line in f.readlines():
            line = line.decode('utf-8').strip('\r\n ')
            if line:
                input_queue.put(line)


if __name__ == "__main__":
    url_queue = Queue()
    get_tasks(url_queue)
    threading_count = 5
    threading_objs = []

    for i in range(threading_count):
        get_repo = GetRepo(url_queue)
        get_repo.start()
        threading_objs.append(get_repo)

    for it in threading_objs:
        it.join()




