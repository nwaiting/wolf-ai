import os
import requests
from lxml import etree
import time
import random
import threading
import logging

logging.basicConfig(level=logging.INFO,
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


class PullRequestHandle(object):
    def __init__(self, pull_url):
        self._pull_url = pull_url

    def run(self):
        pass


class IssueHandle(object):
    def __init__(self, issue_url):
        self._issue_url = issue_url

    def run(self):
        pass


class CommiterHandle(object):
    def __init__(self, commit_url):
        self._commit_url = commit_url

    def get_first_page(self):
        url = 'https://github.com/tensorflow/tensorflow/commits/{}'.format('')
        headers = {
            "Host": "github.com",
            "If-None-Match": 'W/"e13fd2a7072437a5541964a18151f4d7"',
            "Referer": "https://github.com/tensorflow/tensorflow",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"
        }

        url = 'https://github.com/tensorflow/tensorflow/commits/master?after=c5e13d84ca6da4bfc6a190c649f35e7c15154121+34&branch=master'

        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            html = etree.HTML(res.text)
            li_items = html.xpath('//div[@class="TimelineItem-body"]/ol/li')
            for li_item in li_items:
                show_text = li_item.xpath('./div[@class="flex-auto min-width-0"]/p/a/text()')
                show_text = show_text[0] if show_text else ''
                commit_url = li_item.xpath('./div[@class="flex-auto min-width-0"]/p/a/@href')
                commit_url = commit_url[0] if commit_url else ''
                commit_id = os.path.basename(commit_url)
                commitor = li_item.xpath('.//div[@class="f6 text-gray min-width-0"]/a/text()')
                commitor = commitor[0] if commitor else ''
                commit_time = li_item.xpath('.//div[@class="f6 text-gray min-width-0"]/relative-time/@datetime')
                commit_time = commit_time[0] if commit_time else ''
                print("{} = {} = {} = {} = {}".format(commitor, commit_time, commit_id, commit_url, show_text))

    def run(self):
        pass


class GetRepo(object):
    def __init__(self, repo_url):
        self._repo_url = repo_url
        self._branch_versions = []
        self._commiter_handle = CommiterHandle('')
        self._issue_handle = IssueHandle('')
        self._pull_request_handle = PullRequestHandle('')

    def get_versions(self):
        for i in range(1, 200):
            url = 'https://github.com/tensorflow/tensorflow/branches/all?page={}'.format(i)
            headers = {
                "Host": "github.com",
                "If-None-Match": 'W/"e13fd2a7072437a5541964a18151f4d7"',
                "Referer": "https://github.com/tensorflow/tensorflow",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": random.choice(user_agent_list)
            }
            res = ''
            try:
                res = requests.get(url, headers=headers)
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

    def run(self):
        pass


if __name__ == "__main__":
    get_repo = GetRepo('')
    get_repo.run()

