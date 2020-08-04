import requests
import time
import random
from lxml import etree
import re


str_set = {'辞职',
           '离开',
           '结束'}


def main(datas):
    url = 'http://www.baidu.com/s'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    for word in datas:
        params = {
            "ie": "utf-8",
            "cl": "3",
            "mod": "1",
            "isbd": "1",
            "isid": "A801978E9BB34868",
            "f": "8",
            "rsv_bp": "1",
            "rsv_idx": "2",
            "tn": "baiduhome_pg",
            "wd": "{}".format(word),
            "bs": "{}".format(word),
            "rsv_spt": "1",
            "rsv_pq": "c666451600029c2c",
            "rqlang": "cn",
            "rsv_enter": "0",
            "rsv_dl": "tb",
            "rsv_btype": "t",
            "rsv_sid": "undefined",
            "_ss": "1",
            "clist": "",
            "hsug": "",
            "f4s": "1",
            "csor": "0",
            "_cr1": "39593"
        }

        try:
            res = requests.get(url, headers=headers, params=params)
            html = etree.HTML(res.text)
            for item in html.xpath('//div[@class="result c-container "]'):
                item_str = item.xpath('string(./div[@class="c-abstract"])')
                for set_item in str_set:
                    if re.findall(set_item, item_str):
                        print(item_str)
        except Exception as e:
            print('err {}'.format(e))
        else:
            pass
        finally:
            time.sleep(random.randint(1, 4))


if __name__ == '__main__':
    words = ['万科A 王石', '沙河股份 杨建达']
    main(words)




