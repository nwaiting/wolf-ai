import hashlib
import requests
import time
import json
import re
from urllib.parse import quote
import logging
import random
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import datetime
import threading
from queue import Queue
import os
from lxml import etree
from sqlmodel import SqlModel
from config import mobile_user_agents


logging.basicConfig( level=logging.INFO,
    format=('[%(levelname)s %(asctime)s.%(msecs)03d] [%(process)d:%(threadName)s:%(funcName)s:%(lineno)d] %(message)s'),
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__file__)


class GeneratorTask(threading.Thread):
    def __init__(self, q, q_du, dbhost, dbport, dbuser, dbpwd, db):
        self.task_queue = q
        self.task_queue_du = q_du
        self.dbhost = dbhost
        self.dbport = dbport
        self.dbuser = dbuser
        self.dbpwd = dbpwd
        self.db = db
        self.sql = SqlModel(dbhost, dbport, dbuser, dbpwd, db)
        super(GeneratorTask, self).__init__()

    def run(self):
        logger.info("start thread {}".format(self.__class__))
        while True:
            if self.task_queue.qsize() >= 1 and self.task_queue_du.qsize() >= 1:
                time.sleep(1)
                continue

            if self.task_queue.qsize() < 1:
                res = self.sql.get_goods(0, 20)
                for it in res:
                    self.task_queue.put((it['id'], it['productId']))

            if self.task_queue_du.qsize() < 1:
                res = self.sql.get_good_ids(0, 20)
                for it in res:
                    self.task_queue_du.put((it['id'], it['good_id']))


class UpdateResults(threading.Thread):
    def __init__(self, q, q_du, dbhost, dbport, dbuser, dbpwd, db):
        self.task_queue = q
        self.task_queue_du = q_du
        self.dbhost = dbhost
        self.dbport = dbport
        self.dbuser = dbuser
        self.dbpwd = dbpwd
        self.db = db
        self.sql = SqlModel(dbhost, dbport, dbuser, dbpwd, db)
        super(UpdateResults, self).__init__()

    def run(self):
        logger.info("start thread {}".format(self.__class__))
        while True:
            if self.task_queue.empty() and self.task_queue_du.empty():
                time.sleep(1)
                continue

            if not self.task_queue.empty():
                item = self.task_queue.get()
                sql = 'update tb_goods set good_id=%s, sold_items=%s where id=%s'
                args = [item[1], item[2], item[0]]
                try:
                    self.sql.execute_autocommit(sql, args)
                except Exception as e:
                    logger.error("{} {} {}".format(sql, args, e))

            if not self.task_queue_du.empty():
                item = self.task_queue_du.get()
                sql = 'update tb_goods set du_count=%s,du_price=%s,extern=%s where id=%s'
                args = [item[1], item[2], item[3], item[0]]
                try:
                    self.sql.execute_autocommit(sql, args)
                except Exception as e:
                    logger.error("{} {} {}".format(sql, args, e))


class BaseGet(threading.Thread):
    def __init__(self, _dbhost, _dbport, _dbuser, _dbpwd, _db, _sleep=4):
        self.dbhost = _dbhost
        self.dbport = _dbport
        self.dbuser = _dbuser
        self.dbpwd = _dbpwd
        self.cookies = None
        self.api_key = None
        self.db = _db
        self.sql = SqlModel(_dbhost, _dbport, _dbuser, _dbpwd, _db)
        self.sleep = _sleep
        super(BaseGet, self).__init__()

    def get_headers(self):
        return {
            "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            "referer": "https://www.nike.com/"
        }

    def get_cookie(self):
        results = {}
        url = 'https://www.nike.com/'
        request_cookies = {
            "AnalysisUserId": "36.156.80.14.148521598184375620",
            "anonymousId": "769C32991B200F9FC3B7DFD74B6ACBAE",
            "s_ecid": "MCMID%7C29680125002922209910143357000557337455",
            "AMCV_F0935E09512D2C270A490D4D%40AdobeOrg": "1994364360%7CMCMID%7C29680125002922209910143357000557337455%7CMCAID%7CNONE%7CMCOPTOUT-1598191579s%7CNONE%7CvVersion%7C3.4.0",
            "RES_TRACKINGID": "942676271717905",
            "guidS": "cda17c88-60db-4990-cbed-e20ab52c6b9e",
            "guidU": "30953ad3-63fd-4b4f-ca1a-754cdf421726",
            "_gscu_207448657": "981843823r5e6o16",
            "_smt_uid": "5f425bbf.132a70ad",
            "_ga": "GA1.2.65616544.1598184385",
            "geoloc": "cc=CN,rc=SH,tp=vhigh,tz=GMT+8,la=31.22,lo=121.46",
            "NIKE_COMMERCE_COUNTRY": "CN",
            "NIKE_COMMERCE_LANG_LOCALE": "zh_CN",
            "nike_locale": "cn/zh_cn",
            "irclickid": "",
            "Hm_lvt_ed406c6497cc3917d06fd572612b4bba": "{}".format(int(time.time())),
            "_qzjc": "1",
            "_gscbrs_207448657": "1",
            "IR_gbd": "nike.com",
            "IR_PI": "5a6c6a55-331b-11eb-a946-027a93a1e5f2%7C1606834213499",
            "_gcl_au": "1.1.572494435.{}".format(int(time.time())),
            "_gid": "GA1.2.39282147.{}".format(int(time.time())),
            "ResonanceSegment": "1",
            "ppd": "homepage|nikecom>homepage",
            "_uetsid": "5a4fb6a0331b11ebb4c653ebe29219db",
            "_uetvid": "5a4ff120331b11eb894ae5127797ff93",
            "Hm_lpvt_ed406c6497cc3917d06fd572612b4bba": "{}".format(int(time.time())),
            "IR_11873": "1606751311897%7C2432075%7C1606747813499%7C%7C",
            "_qzja": "1.418178858.1598184475796.1606747812730.1606751249596.1606751312174.1606751312183..0.0.11.3",
            "RT": 'z=1&dm=nike.com&si=ae062077-3916-4589-9504-f0b522dbbeaa&ss=ki4pb9j2&sl=0&tt=0&bcn=%2F%2F684d0d3d.akstat.io%2F&ul=1f8dbn&hd=1f8dcp',
            "AKA_A2": "A",
            "bm_sz": "02E43F15725C6A4170E66A21977E2782~YAAQZfaxdRyNGBh2AQAAJbXgHglOIwkhyAPYOdLrOZLLtL0v5edk3QmuZuCxz1BShsqpejDZXwGsn4JOulce1ZkOkzQy74opycYAYPypSjxGOtU9s/GMmqdDY9bYtmVRkiLOc951jXq0yapOKV0IoUn2CxHJSHPukaqV1cpHyp0+bgvwRJ1fGH1+xXOUJsn+apEXCpAEip8I5IQyPyepRw+DX4GRGatUsF9sq8KmVNfMRGGM2ugv9JpA+g8xvxRnDEU4XWTrSWWIDykpf2T8oc074RfODy3ukcQ=",
            "_abck": "A96D1EC0B778990A049A64DE1E674A5D~-1~YAAQZfaxdR2NGBh2AQAAJbXgHgTucvHX8DChiIFdTeP1T/mpsDhfaZbJ4XwmHNOHLAmDLmpBXeGBjfz7tYzF22NhZcIBdXKBjeklg5IJc7VYU7Dgs5J7hCaNcxrjYCXDX0/fSUWM2SVIBtLPGtIoGo5N6uvyoxTBa9DiQmW20GXzfdwSFghq0KalPxY6Uko+rgq+25V3qsvxwpyYWL+umUCowdbZaiQk2rWy1TfClMjYhy+SI7ObyXZc68yWaRQ7ahfO+6fGC0WZReT5mv8swc71mdDM/iliBko8+WR22muWqeGVSnW0Q8B2F4CSPUjIvN3Lb4G8KenLvpxLQ+f2aFeetc9YSs4JYQZUgQ2GEjnyHJCErcfduZbouYVjeYqHbZehsvtCE846IdrUl6LvsMw+LcaoBQtsRwOy8PIT8Jlwpw9qn73MzOYg5KBp4XaPOxPZKIX7H1YXDbuECXxA9HSCcdsu7Ier3g==~-1~-1~-1"
        }

        res = self.get(url, headers=self.get_headers(), cookies=request_cookies)
        if res:
            return requests.utils.dict_from_cookiejar(res.cookies)
        return results

    def get(self, url, headers=None, params=None, cookies=None):
        for _ in range(3):
            try:
                return requests.get(url, headers=headers, params=params, cookies=cookies, timeout=5)
            except Exception as e:
                logger.error("{} {}".format(url, e))
                self.maybe_sleep()
        return []

    def maybe_sleep(self):
        time.sleep(random.uniform(0, self.sleep))

    def maybe_sleep5to10(self):
        time.sleep(random.uniform(5, 10))

    def save(self, datas):
        self.sql.add_goods(datas)


class JDGet(BaseGet):
    def __init__(self, pro_dict, dbhost, dbport, dbuser, dbpwd, db):
        self.products_dict = pro_dict
        super(JDGet, self).__init__(dbhost, dbport, dbuser, dbpwd, db)

    def get_page(self):
        url = 'https://search.jd.com/s_new.php'
        headers = {
            "referer": "https://search.jd.com/Search",
            "user-agent": 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36',
            "x-requested-with": "XMLHttpRequest"
        }
        params = {
            "keyword": "m2k",
            "wq": "m2k",
            "page": "7",
            "s": "178",
            "click": "0"
        }
        res = self.get(url, headers=headers, params=params)

        html = etree.HTML(res.text)
        for item in html.xpath('//li[@class="gl-item"]'):
            title = item.xpath('.//div[@class="p-img"]/a/@title')[0]
            price = float(item.xpath('.//div[@class="p-price"]/strong/i/text()')[0])
            for item1 in item.xpath('.//div[@class="p-scroll"]//li[@class="ps-item"]/a'):
                title_litte = item1.xpath('./@title')[0]
                productId = item1.xpath('./img/@data-sku')[0] if item1.xpath('./img/@data-sku') else ''
                url = "https://item.jd.com/{}.html".format(productId)
                img_url = item1.xpath('./img/@src') or item1.xpath('./img/@data-lazy-img') or item1.xpath(
                    './img/@data-lazy-img-slave')
                pic = "https:{}".format(img_url[0])



    def first_get(self, k, url):
        results = []
        params_next = ''
        totalPages = 0
        res = self.get(url, headers=self.get_headers(), cookies=self.get_cookie())
        if res:
            re_pattern = re.compile(r"<script>window.INITIAL_REDUX_STATE=(.*?);</script>")
            json_str = json.loads(re_pattern.findall(res.text)[0])
            params_next = json_str['Wall']['pageData']['next']
            totalPages = json_str['Wall']['pageData']['totalPages']
            totalResources = json_str['Wall']['pageData']['totalResources']
            for ite in json_str['Wall']['products']:
                salesChannel = ite.get('salesChannel', [])
                for ite_inner in ite['colorways']:
                    results.append({
                        "title": ite['subtitle'],
                        "url": self.get_details_page(ite_inner['pdpUrl']),
                        'salesChannel': salesChannel,
                        'good_id': os.path.basename(ite_inner['pdpUrl']),
                        'productId': ite_inner['cloudProductId'],
                        'pic': ite_inner['images']['squarishURL'],
                        'price': ite_inner['price']['currentPrice'],
                        'fullPrice': ite_inner['price']['fullPrice']
                    })
            logger.info("{} total pages:{}, totalsource:{}".format(k, totalPages, totalResources))
        return params_next, totalPages, '', results

    def get_products(self, k, vals):
        params = {}
        for i in range(200):
            pass









        params_next, totalPages, id, results = self.first_get(k, vals['url'])
        self.save(results)
        for i in range(totalPages):
            url = ''
            params = {
                "queryid": "products",
                "anonymousId": vals['anonymousId'],
                "country": "cn",
                "endpoint": params_next,
                "language": "zh-Hans",
                "localizedRangeStr": "{lowestPrice} — {highestPrice}"
            }
            tmp_list = []
            res = self.get(url, headers=self.get_headers(), params=params, cookies=self.get_cookie())
            params_next = res.json()['Wall']['pageData']['next']
            for ite in res:
                tmp_list.append({

                })
            self.save(tmp_list)
            logger.info("add {} {}".format(k, len(tmp_list)))
            self.maybe_sleep()

    def run(self):
        while True:
            for k, v in self.products_dict.items():
                self.get_products(k, v)
            self.maybe_sleep5to10()


class SearchVIPGet(BaseGet):
    def __init__(self, _keys_list, dbhost, dbport, dbuser, dbpwd, db):
        self.keys_list = _keys_list
        super(SearchVIPGet, self).__init__(dbhost, dbport, dbuser, dbpwd, db)

    def get_ids(self, key_word):
        results_list = []
        for i in range(50):
            per_count = 200
            url = "https://mapi.vip.com/vips-mobile/rest/shopping/pc/search/product/rank"
            params = {
                "callback": "getMerchandiseIds",
                "app_name": "shop_pc",
                "app_version": "4.0",
                "warehouse": "VIP_SH",
                "fdc_area_id": "931101113121",
                "client": "pc",
                "mobile_platform": "1",
                "province_id": "103101",
                "api_key": self.api_key,
                "user_id": "",
                "mars_cid": "1605533789294_e23f274b271b6897ed83c52cad62f1f0",
                "wap_consumer": "a",
                "standby_id": "nature",
                "keyword": key_word,
                "lv3CatIds": "",
                "lv2CatIds": "",
                "lv1CatIds": "",
                "brandStoreSns": "",
                "props": "",
                "priceMin": "",
                "priceMax": "",
                "vipService": "",
                "sort": "0",
                "pageOffset": "{}".format(i * per_count),
                "channelId": "1",
                "gPlatform": "PC",
                "batchSize": "{}".format(per_count),
                "_": "{}".format(int(time.time()) * 1000)
            }
            try:
                res = self.get(url, headers=self.get_headers(), params=params)
                res_json = {}
                find_str = 'getMerchandiseIds('
                if res.text.startswith(find_str):
                    res_json = json.loads(res.text[len(find_str):-1])

                tmp_list = [it['pid'] for it in res_json['data']['products']]
                results_list.extend(tmp_list)
                logger.info("{} get ids {}:{}".format(self.__class__, key_word, len(results_list)))
                if len(tmp_list) < per_count - 10:
                    break
            except Exception as e:
                logger.error("{} {}:{} {}".format(self.__class__, url, i, e))
                break
            else:
                time.sleep(random.uniform(0, 4))
        return results_list

    def get_products(self, key_word):
        product_ids = self.get_ids(key_word)
        logger.info("{} {} products:{}".format(self.__class__, key_word, len(product_ids)))

        ts = int(time.time()) * 1000
        url = 'https://mapi.vip.com/vips-mobile/rest/shopping/pc/product/module/list/v2'

        for i_index in range(1000):
            begin_index = i_index * 50
            end_index = (i_index + 1) * 50
            if begin_index >= len(product_ids):
                break
            params = {
                "callback": "getMerchandiseDroplets1",
                "app_name": "shop_pc",
                "app_version": "4.0",
                "warehouse": "VIP_SH",
                "fdc_area_id": "103101101",
                "client": "pc",
                "mobile_platform": "1",
                "province_id": "103101",
                "api_key": "{}".format(self.api_key),
                "user_id": "",
                "mars_cid": "1604906927034_08fa7a00d3c9cd0288978fe43e69bb46",
                "wap_consumer": "a",
                "productIds": '{}'.format(','.join(product_ids[begin_index:end_index])),
                "scene": "brand",
                "standby_id": "nature",
                "extParams": json.dumps({"multiBrandStore": "", "stdSizeVids": "", "subjectId": "", "brandId": "", "preheatTipsVer": "3",
                            "couponVer": "v2", "exclusivePrice": "1", "iconSpec": "2x"}),
                "context":"",
                "_": "{}".format(ts)
            }

            products_infos = []
            try:
                # res = requests.get(url, params=params, headers=self.headers, cookies=cookies)
                res = self.get(url, params=params, headers=self.get_headers(), cookies=self.cookies)
                datas = res.text
                if datas.startswith('getMerchandiseDroplets1('):
                    datas = json.loads(datas[len('getMerchandiseDroplets1('):-1])

                for d in datas['data']['products']:
                    # if d['title'].find('鞋') == -1:
                    #     continue
                    products_infos.append(("{}-{}".format(d['brandId'], d['productId']), d['brandId'], d['productId'], '',
                                           d['title'], d['smallImage'],
                                           self.get_detail_url(d['brandId'], d['productId']),d['price']['saleDiscount'],
                                           self.get_discount(d['price']['saleDiscount']), to_float(d['price']['salePrice']),
                                           to_float(d['price']['marketPrice']), ','.join([it.get('value', '') for it in d.get('labels', [])]),
                                           "search_{}".format(key_word), 0, 0, json.dumps({}), int(time.time()),
                                           datetime.datetime.now(), datetime.datetime.now().strftime("%Y-%m-%d")
                                           ))
            except Exception as e:
                logger.error("{}:{}:{}".format(self.__class__, url, e))

            if products_infos:
                self.save(products_infos)
                logger.info("add {} {}".format("search_{}".format(key_word), len(products_infos)))
            time.sleep(random.uniform(0, 4))

    def run(self):
        logger.info("start thread {}".format(self.__class__))
        while True:
            res = self.init()
            if not res:
                time.sleep(2)
            else:
                break
        while True:
            for it in self.keys_list:
                self.get_products(it)
            time.sleep(1)


if __name__ == '__main__':
    # goods_dict = {
    #     '100782909': 'nike',
    #     '100781965': 'nike_sport',
    #     '100782915': 'vans',
    #     '100782928': 'adidas',
    #     '100707713': 'adidas_neo',
    #     '100782923': 'adidas_sport',
    # }
    #
    # search_list = [
    #     'ah2613',
    # ]
    #
    # works = []
    # tasks_detail = Queue(1000)
    # results_detail = Queue(1000)
    # tasks_du = Queue(1000)
    # results_du = Queue(1000)
    # dbhost = '192.168.2.132'
    # dbport = 3306
    # dbuser = ''
    # dbpwd = ''
    # db = 'goods'
    # mailhost = 'smtp.qq.com'
    # mailpwd = ''
    # mailsender = '798990255@qq.com'
    # mailreceivers = ['798990255@qq.com']
    # vip = VipGet(goods_dict, dbhost, dbport, dbuser, dbpwd, db)
    # works.append(vip)
    #
    # update_result = UpdateResults(results_detail, results_du, dbhost, dbport, dbuser, dbpwd, db)
    # works.append(update_result)
    #
    # generator_task = GeneratorTask(tasks_detail, tasks_du, dbhost, dbport, dbuser, dbpwd, db)
    # works.append(generator_task)
    #
    # params = {
    #     "delta": 30,
    #     "delta_count": 800,
    #     "discount": 3,
    #     "discount_count": 1000,
    #     "lowprice_delta": 100,
    #     "lowprice_delta_count": 100
    # }
    # mail_task = MailNotify(dbhost, dbport, dbuser, dbpwd, db, mailhost, mailpwd, mailsender, mailreceivers, params)
    # works.append(mail_task)
    #
    # search_vip = SearchVIPGet(search_list, dbhost, dbport, dbuser, dbpwd, db)
    # works.append(search_vip)
    #
    # for _ in range(4):
    #     d = DuGet(tasks_du, results_du)
    #     works.append(d)
    #
    # for _ in range(4):
    #     d = GoodDetailGet(tasks_detail, results_detail)
    #     works.append(d)
    #
    # for it in works:
    #     it.start()
    #
    # for it in works:
    #     it.join()
    # logger.log("结束!!")


    # url = 'https://www.nike.com/cn/w/womens-apparel-5e1x6z6ymx6'
    # headers = {
    #     "referer": "https://www.nike.com/cn/w/womens-best-5e1x6z76m50",
    #     "user-agent": random.choice(user_agent_list)
    # }
    # res = requests.get(url, headers=headers)
    # print(res.status_code)
    # print(res.text)


    url = 'https://module-jshop.jd.com/module/allGoods/goods.html'
    headers = {
        "referer": "https://search.jd.com/Search",
        "user-agent": 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36',
        "x-requested-with": "XMLHttpRequest"
    }
    params = {
        "callback": " jQuery7958364",
        "sortType": " 0",
        "appId": " 1005989",
        "pageInstanceId": " 103275864",
        "searchWord": "",
        "pageNo": " 3",
        "direction": " 1",
        "instanceId": " 245423702",
        "modulePrototypeId": " 55555",
        "moduleTemplateId": " 905542",
        "refer": " https://mall.jd.com/view_search-1005989-11073177-99-1-24-1.html",
        "_":"1608395338886",
    }
    res = requests.get(url, headers=headers, params=params)
    print(res.status_code)
    # print(res.text)
    res_json = json.loads(res.text.replace('jQuery7958364(', '')[:-1])


    import os
    import sys
    sys.exit(0)
    url = 'https://search.jd.com/s_new.php'
    headers = {
        "referer": "https://search.jd.com/Search",
        "user-agent": 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36',
        "x-requested-with": "XMLHttpRequest"
    }
    params = {
        "keyword": "adidas官方旗舰店",
        "enc": "utf-8",
        "suggest": "5.def.0.base",
        "wq": "adi",
        # "pvid": "5831304637e840d0bc0a26a4af72c2f4"
    }
    res = requests.get(url, params=params, headers=headers)
    print(res.status_code)
    print(requests.utils.dict_from_cookiejar(res.cookies))
    print(res.text)
    with open("{}.html".format(time.time()), "wb") as f:
        f.write(res.text.encode('utf-8'))
    from lxml import etree
    html = etree.HTML(res.text)
    results = []
    for item in html.xpath('//li[@class="gl-item"]'):
        title = item.xpath('.//div[@class="p-img"]/a/@title')[0]
        price = float(item.xpath('.//div[@class="p-price"]/strong/i/text()')[0])
        for item1 in item.xpath('.//div[@class="p-scroll"]//li[@class="ps-item"]/a'):
            title_litte = item1.xpath('./@title')[0]
            tmp_id = item1.xpath('./img/@data-sku')[0] if item1.xpath('./img/@data-sku') else ''
            src = "https://item.jd.com/{}.html".format(tmp_id)
            img_url = item1.xpath('./img/@src') or item1.xpath('./img/@data-lazy-img') or item1.xpath('./img/@data-lazy-img-slave')
            pic = "https:{}".format(img_url[0])
            results.append({})
        print('='*32)
    if len(results) <= 0:
        print("店铺结束")

    # import re
    # re_pattern = re.compile(r"<script>window.INITIAL_REDUX_STATE=(.*?);</script>")
    # json_str = json.loads(re_pattern.findall(res.text)[0])
    # # print(re_pattern.findall(res.text)[0])
    # print(json_str['Wall']['pageData'])
    # for ite in json_str['Wall']['products']:
    #     print(ite)

