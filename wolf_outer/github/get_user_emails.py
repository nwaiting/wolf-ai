import requests
from lxml import etree
import time
import random


def main():

    headers = {
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Host": "github.com",
        "If-None-Match": 'W/"7b61ea5255dc063b84fda0da02d5b7b7',
        "Referer": "https://github.com/search?q=%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0&type=Issues",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
        "X-PJAX": "true",
        "X-PJAX-Container": "#js-pjax-container",
        "X-Requested-With": "XMLHttpRequest"
    }

    cookie = {
        "_ga":"GA1.2.872094573.1500740616",
        "_device_id":"27519fe57a68f1458ad08f40322eff4f",
        "_octo":"GH1.1.1188686479.1564068663",
        "tz":"Asia%2FShanghai",
        "has_recent_activity":"1",
        "_gid":"GA1.2.554941860.1595950562",
        "user_session":"",
        "__Host-user_session_same_site":"",
        "logged_in":"yes",
        "dotcom_user":"nwaiting",
        " _gat":"1",
        "_gh_sess":""
    }

    url = 'https://github.com/search'
    params = {
        "q": '机器学习',
        'type': "Issues",
        '_pjax': '#js-pjax-container'
    }

    for i in range(1, 101):
        params['p'] = i
        res = requests.get(url, params=params, cookies=cookie, headers=headers)
        print(res.status_code, len(res.text))
        # print(res.text)

        html = etree.HTML(res.text)
        items = html.xpath('//div[@class="ml-1 flex-auto "]')
        user_name_set = set()
        for item in items:
            user_name = item.xpath('./div[@class="text-small"]/a[1]/text()')[0]
            find_index = user_name.find('/')
            if find_index != -1:
                user_name = user_name[:find_index]
                user_name_set.add(user_name)
            user_name = item.xpath('.//div[@class="d-inline mr-3"]/a/text()')[0]
            user_name_set.add(user_name)

        for name in user_name_set:
            url = "https://github.com/{}".format(name)
            res = requests.get(url)
            print(res.status_code, len(res.text))

            if res.status_code == 200:
                html = etree.HTML(res.text)
                items = html.xpath('//ul[@class="vcard-details"]/li')
                for item in items:
                    txt = item.xpath('string(.)').strip('\r\n ')
                    print(txt)
            time.sleep(random.randint(1, 3))
        time.sleep(random.randint(1, 3))






if __name__ == "__main__":
    main()





