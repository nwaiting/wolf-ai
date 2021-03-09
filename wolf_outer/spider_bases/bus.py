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
import pymysql
from pymysql.cursors import DictCursor
from DBUtils.PersistentDB import PersistentDB
import datetime
import threading
from queue import Queue

logging.basicConfig(level=logging.INFO,
    format=('[%(levelname)s %(asctime)s.%(msecs)03d] [%(process)d:%(threadName)s:%(funcName)s:%(lineno)d] %(message)s'),
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__file__)


def get_proxy():
    select_proxy_address = '182.96.170.113:65000'
    requests_proxy = {
        'http': "http://0902gl1t1m651:0902gl1t1m651@{}".format(select_proxy_address),
        'https': "https://0902gl1t1m651:0902gl1t1m651@{}".format(select_proxy_address)
    }
    requests_proxy = None
    return requests_proxy


user_agent_list = [
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
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.17) Gecko/20110123 (like Firefox/3.x) SeaMonkey/2.0.12",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36"
]


def to_int(v, default=0):
    try:
        return int(v)
    except:
        return default


def to_float(v, default=0.0):
    try:
        return float(v)
    except:
        return default


class SqlModel(object):
    def __init__(self, host, port, user, passwd, name, charset='utf8mb4'):
        self._db_host = host
        self._db_port = port
        self._db_user = user
        self._db_passwd = passwd
        self._db_name = name
        self._db_charset = charset
        self._pool = None

    @property
    def conn(self):
        if not self._pool:
            self._pool = PersistentDB(creator=pymysql,
                             host=self._db_host,
                             port=self._db_port,
                             user=self._db_user,
                             passwd=self._db_passwd,
                             db=self._db_name,
                             charset=self._db_charset,
                             cursorclass=DictCursor)
        retry = 0
        while retry < 100:
            try:
                return self._pool.connection()
            except AttributeError:
                retry += 1
                logger.warning('retry _pool.connection %d' % retry)
                time.sleep(1)

    def execute(self, sql, args=None):
        with self.conn as conn, conn.cursor() as cur:
            cur.execute(sql, args=args)
            return list(cur.fetchall())

    def execute_autocommit(self, sql, args=None):
        with self.conn as conn, conn.cursor() as cur:
            cur.execute(sql, args=args)
            conn.commit()

    def add_goods(self, datas):
        with self.conn as conn, conn.cursor() as cur:
            sql = 'insert into tb_goods(uuid,brandId,productId,good_id,title,pic,detail,saleDiscount,discount,price,' \
                  'marketPrice,source_extern,source,du_price,du_count,extern,updated_ts,updated_date,updated_day) ' \
                  'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update updated_ts=values(updated_ts)'
            try:
                cur.executemany(sql, datas)
                conn.commit()
            except Exception as e:
                logger.error("{} {}".format(e, datas))

    def get_goods(self, limit, size, prod_type=None):
        def _format_condition():
            where = []
            args = []
            where.append('updated_day=%s')
            args.append(datetime.datetime.now().strftime('%Y-%m-%d'))
            if prod_type:
                where.append('prod_type=%s')
                args.append(prod_type)
            where.append("good_id=''")

            where = ('where ' + (' and '.join(where))) if where else ''
            return where, args

        with self.conn as conn, conn.cursor() as cur:
            conditions, arg = _format_condition()
            sql = 'select id,productId from tb_goods {} order by updated_ts desc limit %s,%s'.format(conditions)
            cur.execute(sql, arg + [limit, size])
            return list(cur.fetchall())

    def get_good_ids(self, limit, size, prod_type=None):
        def _format_condition():
            where = []
            args = []
            where.append('updated_day=%s')
            args.append(datetime.datetime.now().strftime('%Y-%m-%d'))
            if prod_type:
                where.append('prod_type=%s')
                args.append(prod_type)
            where.append("good_id!='' and du_count=0")

            where = ('where ' + (' and '.join(where))) if where else ''
            return where, args

        with self.conn as conn, conn.cursor() as cur:
            conditions, arg = _format_condition()
            sql = 'select id,good_id from tb_goods {} order by updated_ts desc limit %s,%s'.format(conditions)
            cur.execute(sql, arg + [limit, size])
            return list(cur.fetchall())


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


class GoodDetailGet(threading.Thread):
    def __init__(self, task_q, result_q, sleep=4):
        self.task_queue = task_q
        self.result_queue = result_q
        self.sleep =sleep
        super(GoodDetailGet, self).__init__()

    def get_headers(self):
        return {
                "user-agent": random.choice(user_agent_list),
                "referer": "https://list.vip.com/"
                }

    def get_sold_detail(self, productId):
        url = 'https://stock.vip.com/detail/'
        params = {
            "callback": "stock_detail",
            "merchandiseId": productId,
            "is_old": "0",
            "areaId": "103101",
            "_": "{}".format(int(time.time() * 1000))
        }

        r = []
        try:
            if get_proxy():
                res = requests.get(url, headers=self.get_headers(), params=params, timeout=5, proxies=get_proxy())
            else:
                res = requests.get(url, headers=self.get_headers(), params=params, timeout=5)
            contents = res.text.replace("stock_detail(", '').strip('\r\n ')[:-1]
            c2 = json.loads(contents)
            for it in c2['items']:
                if int(it.get('stock', 0)) > 0:
                    r.append({
                        it['name']: it['stock']
                    })
            return json.dumps(r)
        except Exception as e:
            logger.error("get_sold_detail {}={}={}".format(url, productId, e))
        return json.dumps(r)

    def get_detail(self, productId, api_key='70f71280d5d547b2a7bb370a529aeea1'):
        url = 'https://mapi.vip.com/vips-mobile/rest/shopping/pc/product/detail/v5'
        params = {
            "callback": "detailInfoCB",
            "app_name": "shop_pc",
            "app_version": "4.0",
            "warehouse": "VIP_SH",
            "fdc_area_id": "103101101",
            "client": "pc",
            "mobile_platform": "1",
            "province_id": "103101",
            "api_key": "{}".format(api_key),
            "user_id": "",
            "mars_cid": "1604906927034_08fa7a00d3c9cd0288978fe43e69bb46",
            "wap_consumer": "a",
            "productId": "{}".format(productId),
            "functions": "brand_store_info,newBrandLogo,hideOnlySize,extraDetailImages,sku_price,ui_settings",
            "kfVersion": "1",
            "highlightBgImgVer": "1",
            "is_get_TUV": "1",
            "commitmentVer": "2",
            "haitao_description_fields": "text",
            "supportSquare": "1",
            "longTitleVer": "2",
            "propsVer": "1"
        }
        try:
            if get_proxy():
                res = requests.get(url, headers=self.get_headers(), params=params, timeout=5, proxies=get_proxy())
            else:
                res = requests.get(url, headers=self.get_headers(), params=params, timeout=5)
            contents = res.text.replace('detailInfoCB(', '').strip('\r\n ')[:-1]
            c = json.loads(contents)
            return c['data']['product']['merchandiseSn']
        except Exception as e:
            logger.error("get_detail {}={}={}".format(url, productId, e))
        return ''

    def run(self):
        logger.info("start thread {}".format(self.__class__))
        statistic_count = 0
        while True:
            if self.task_queue.empty():
                time.sleep(1)
                continue
            items = self.task_queue.get()
            db_id, product_id = items[0], items[1]
            good_id = self.get_detail(product_id)
            sold_items = self.get_sold_detail(product_id)
            self.result_queue.put((db_id, good_id, sold_items))
            statistic_count += 1
            if statistic_count % 100 == 0:
                logger.info("{} done {}, current {}:{}".format(self.__class__, statistic_count,
                                                               self.task_queue.qsize(), self.result_queue.qsize()))
            time.sleep(random.uniform(0, self.sleep))


class DuGet(threading.Thread):
    def __init__(self, task_q, results_q, sleep=4):
        self.task_queue = task_q
        self.results_queue = results_q
        self.sleep = sleep
        self.headers = {
               'Host': "app.poizon.com",
               'User-Agent': "{} MicroMessenger/7.0.4.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat".format(random.choice(user_agent_list)),
               'appid': "wxapp",
               'appversion': "4.4.0",
               'content-type': "application/json",
               'Accept-Encoding': "gzip, deflate, br",
               'Accept': "*/*",
           }

        index_load_more_url = 'https://app.poizon.com/api/v1/h5/index/fire/index'
        # {"sign":"5e22051c5156608a85b12d501d615c61","tabId":"","limit":20,"lastId":1}
        recensales_load_more_url = 'https://app.poizon.com/api/v1/h5/commodity/fire/last-sold-list'
        # {"sign":"f44e26eb08becbd16b7ed268d83b3b8c","spuId":"73803","limit":20,"lastId":"","sourceApp":"app"}
        product_detail_url = 'https://app.poizon.com/api/v1/h5/index/fire/flow/product/detail'
        # {"sign":"5721d19afd7a7891b627abb9ac385ab0","spuId":"49413","productSourceName":"","propertyValueId":"0"}
        category = {"code":200,"msg":"success","data":{"list":[{"catId":0,"catName":"品牌"},{"catId":1,"catName":"系列"},{"catId":3,"catName":"球鞋"},{"catId":6,"catName":"潮搭"},{"catId":8,"catName":"手表"},{"catId":1000119,"catName":"配件"},{"catId":7,"catName":"潮玩"},{"catId":9,"catName":"数码"},{"catId":1000008,"catName":"家电"},{"catId":726,"catName":"箱包"},{"catId":587,"catName":"美妆"},{"catId":945,"catName":"家居"}]},"status":200}
        doCategoryDetail = {"code":200,"msg":"success","data":{"list":[{"brand":{"goodsBrandId":144,"brandName":"Nike","type":0,"logoUrl":"https://du.hupucdn.com/news_byte3724byte_94276b9b2c7361e9fa70da69894d2e91_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":13,"brandName":"Jordan","type":0,"logoUrl":"https://du.hupucdn.com/news_byte3173byte_5c87bdf672c1b1858d994e281ce5f154_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":3,"brandName":"adidas","type":0,"logoUrl":"https://du.hupucdn.com/news_byte24108byte_fc70f4c88211e100fe6c29a6f4a46a96_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":494,"brandName":"adidas originals","type":0,"logoUrl":"https://du.hupucdn.com/news_byte24706byte_9802f5a4f25e6cd1b284a5b754cec4f0_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":439,"brandName":"Supreme","type":0,"logoUrl":"https://du.hupucdn.com/news_byte6426byte_c7ab640bf99963bfc2aff21ca4ff8322_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":79,"brandName":"GUCCI","type":0,"logoUrl":"https://du.hupucdn.com/news_byte25670byte_c9ca8b5347750651bebbf84dd7d12d01_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10359,"brandName":"Fear of God","type":0,"logoUrl":"https://du.hupucdn.com/news_byte17196byte_d5f7a627b65e90f6b850b613c14b54a2_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10176,"brandName":"LOUIS VUITTON","type":0,"logoUrl":"https://du.hupucdn.com/news_byte33190byte_d14f21356f020e12a534b967be2bed77_w382h322.png"},"seriesList":[]},{"brand":{"goodsBrandId":1245,"brandName":"OFF-WHITE","type":0,"logoUrl":"https://du.hupucdn.com/news_byte2408byte_4d329f274512ddb136989432292cdd3f_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":45,"brandName":"THE NORTH FACE","type":0,"logoUrl":"https://du.hupucdn.com/news_byte31268byte_e05935a55a37e7901640f7d09548499d_w151h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10082,"brandName":"FOG","type":0,"logoUrl":"https://du.hupucdn.com/news_byte23329byte_3e247b5d598f7da36a1af24d08cb9ad8_w350h350.png"},"seriesList":[]},{"brand":{"goodsBrandId":10215,"brandName":"STONE ISLAND","type":0,"logoUrl":"https://du.hupucdn.com/news_byte24302byte_570d51bb8c62233c3b52a9ffb05e5d74_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10223,"brandName":"HERMES","type":0,"logoUrl":"https://du.hupucdn.com/news_byte30429byte_658ec36fbe99d2b3ae1e5a685ee1b20c_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10370,"brandName":"Jimmy Choo","type":0,"logoUrl":"https://du.hupucdn.com/news_byte18060byte_e664bd98b2a590c464e0e154b5f9ce53_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":1310,"brandName":"Champion","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21403byte_6995f22e76a1a203f4f4dfd3ff43c21b_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":176,"brandName":"Converse","type":0,"logoUrl":"https://du.hupucdn.com/news_byte8272byte_078b04a261c1bb1c868f1522c7ddcefc_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":2,"brandName":"Puma","type":0,"logoUrl":"https://du.hupucdn.com/news_byte26564byte_a768870ae48f1a216dd756c2206c34b1_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":4,"brandName":"New Balance","type":0,"logoUrl":"https://du.hupucdn.com/news_byte6189byte_1cb7717a44b335651ad4656610142591_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":7,"brandName":"Under Armour","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21646byte_0bd049d8c27c8509f3166d68a388dfe9_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":9,"brandName":"Vans","type":0,"logoUrl":"https://du.hupucdn.com/news_byte9507byte_49aaeb534cecab574949cf34b43da3a5_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":33,"brandName":"李宁","type":0,"logoUrl":"https://du.hupucdn.com/news_byte7350byte_d60fa387aac42cb8c9b79700d720397d_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":4981,"brandName":"JRs","type":0,"logoUrl":"https://du.hupucdn.com/news_byte5113byte_7a651984f882e48df46c67758d6934d2_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10027,"brandName":"Dickies","type":0,"logoUrl":"https://du.hupucdn.com/news_byte37984byte_e8d6f32f6b17f736a422fac90c99d7e5_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10113,"brandName":"ANTI SOCIAL SOCIAL CLUB","type":0,"logoUrl":"https://du.hupucdn.com/news_byte28476byte_863a194b02da977009144bd9f10dde1f_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":843,"brandName":"CASIO","type":0,"logoUrl":"https://du.hupucdn.com/news_byte4156byte_4d3d1a6e2beca7f700e1ac92ea6b2fdf_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10141,"brandName":"UNDEFEATED","type":0,"logoUrl":"https://du.hupucdn.com/news_byte16826byte_6d7166e0081d6b42619e54ca06900406_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10250,"brandName":"NINTENDO","type":0,"logoUrl":"https://du.hupucdn.com/news_byte29039byte_b5b91acfeaf88ec0c76df08b08e6e5cd_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10001,"brandName":"Thrasher","type":0,"logoUrl":"https://du.hupucdn.com/news_byte30750byte_446d35e36b912ad366d8f72a6a9cc5e4_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10021,"brandName":"Cav Empt","type":0,"logoUrl":"https://du.hupucdn.com/news_byte61774byte_7a5969f3694fc71f727c63e8bc3d95d5_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10032,"brandName":"Burberry","type":0,"logoUrl":"https://du.hupucdn.com/news_byte27771byte_9031f22329273c84170de8aa0f7d7c67_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10037,"brandName":"C2H4","type":0,"logoUrl":"https://du.hupucdn.com/news_byte42973byte_8681e3b6092a4dbf6938621cb28e75f4_w284h284.png"},"seriesList":[]},{"brand":{"goodsBrandId":10043,"brandName":"Mitchell & Ness","type":0,"logoUrl":"https://du.hupucdn.com/news_byte35794byte_37e1d65f0c9df1c61c217bded6435b9d_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10046,"brandName":"Moncler","type":0,"logoUrl":"https://du.hupucdn.com/news_byte27878byte_9066687c9718c1168f8846653018a935_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":1860,"brandName":"THOM BROWNE","type":0,"logoUrl":"https://du.hupucdn.com/news_byte7866byte_fc0d1f01af88a3425bb106fe21f720a9_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10062,"brandName":"VLONE","type":0,"logoUrl":"https://du.hupucdn.com/news_byte38175byte_da7a862bd765220eb9bb00efbf5cfab3_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10072,"brandName":"HUAWEI","type":0,"logoUrl":"https://du.hupucdn.com/news_byte53433byte_8949768c520c73adfd0798c7416ff642_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10073,"brandName":"Canada Goose","type":0,"logoUrl":"https://du.hupucdn.com/news_byte40959byte_26901c3ba55661a1ea668d49c599e86b_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":1131,"brandName":"隐蔽者","type":0,"logoUrl":"https://du.hupucdn.com/news_byte28746byte_5a165d2728e81983d7bbd59739e56b97_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10095,"brandName":"FMACM","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21768byte_8480a963cd231f2ea4ec032753238cd9_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10098,"brandName":"Onitsuka Tiger","type":0,"logoUrl":"https://du.hupucdn.com/news_byte27415byte_63662423bde0d02cb8576ff47afb270d_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10103,"brandName":"Guuka","type":0,"logoUrl":"https://du.hupucdn.com/news_byte29973byte_ef6eeef0535a0c9b2ade4fb6efc0aa06_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":634,"brandName":"A BATHING APE","type":0,"logoUrl":"https://du.hupucdn.com/news_byte8375byte_cedf2c6ad46d2ac60f0c2f86cbccffcd_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10115,"brandName":"Mishkanyc","type":0,"logoUrl":"https://du.hupucdn.com/news_byte34270byte_f4816f6a78ea1e528144fadcaf671db6_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10119,"brandName":"AMBUSH","type":0,"logoUrl":"https://du.hupucdn.com/news_byte22861byte_44dadd412d9c0b3c57f0d382f5554f5c_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10120,"brandName":"CDG Play","type":0,"logoUrl":"https://du.hupucdn.com/news_byte30859byte_4b1af0b2a9bc9007a3f0c5385fea1f8d_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10164,"brandName":"GOTNOFEARS","type":0,"logoUrl":"https://du.hupucdn.com/news_byte22932byte_c11b6cb93dc1f26ee98d44db6017c522_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10172,"brandName":"THE NORTH FACE PURPLE LABEL","type":0,"logoUrl":"https://du.hupucdn.com/news_byte22025byte_ce1dc9be1690240e01f1365eedac1362_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10186,"brandName":"Subcrew","type":0,"logoUrl":"https://du.hupucdn.com/news_byte23252byte_48b6f7f61cad6c18fb7adafe9696ef1f_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10243,"brandName":"Aftermaths","type":0,"logoUrl":"https://du.hupucdn.com/news_byte20974byte_9b01f95cba8e542a258ccc7f1ccf9647_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10248,"brandName":"Aape","type":0,"logoUrl":"https://du.hupucdn.com/news_byte34614byte_beb0b973078c0e17171edea6cd0c715d_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10263,"brandName":"apm monaco","type":0,"logoUrl":"https://du.hupucdn.com/news_byte28592byte_384295707fe8076c1cc738402f3b928b_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":6,"brandName":"Reebok","type":0,"logoUrl":"https://du.hupucdn.com/news_byte8192byte_cda902674ee7d4d4c51d32b834a76e7b_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10264,"brandName":"DUEPLAY","type":0,"logoUrl":"https://du.hupucdn.com/news_byte20052byte_41e361c6d2df6895d3b38dfdd9c2efa9_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":577,"brandName":"PALACE","type":0,"logoUrl":"https://du.hupucdn.com/news_byte8691byte_5577b630f2fd4fcb8d6f7f45071acc40_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10000,"brandName":"ROARINGWILD","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21733byte_bf73cc451933ed2392d31620c08f76d6_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":1222,"brandName":"NOAH","type":0,"logoUrl":"https://du.hupucdn.com/news_byte33752byte_11638ecd79b8d3c7fd29b92dfb9f5f5b_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10030,"brandName":"Carhartt WIP","type":0,"logoUrl":"https://du.hupucdn.com/news_byte9975byte_222768bbe7d7daffed18c85090de6153_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10298,"brandName":"BANU","type":0,"logoUrl":"https://du.hupucdn.com/news_byte24263byte_c480365559a6a9808a69547bc8084579_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10357,"brandName":"EQUALIZER","type":0,"logoUrl":"https://du.hupucdn.com/news_byte18391byte_b300fb77b24a776296bc7a92873d1839_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10075,"brandName":"RIPNDIP","type":0,"logoUrl":"https://du.hupucdn.com/news_byte35669byte_5e1b7e4e57ee4568bfb9bf657c8146c5_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10087,"brandName":"Stussy","type":0,"logoUrl":"https://du.hupucdn.com/news_byte30589byte_c37b4863d6248dd92a588696c9e1dfe5_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10092,"brandName":"NPC","type":0,"logoUrl":"https://du.hupucdn.com/news_byte5399byte_249e0a587b457f46e7e6bad9fd7234bc_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10118,"brandName":"Red Charcoal","type":0,"logoUrl":"https://du.hupucdn.com/news_byte19757byte_91817a270103c441138260ad9812f1d8_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10106,"brandName":"Dior","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21672byte_cfe86702e27c9870189b6ad6a7f795b8_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":65,"brandName":"Apple","type":0,"logoUrl":"https://du.hupucdn.com/news_byte1253byte_c8fcc08b731e30d4d1453c77bb4417d7_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10039,"brandName":"Randomevent","type":0,"logoUrl":"https://du.hupucdn.com/news_byte22681byte_d422ea97ad63fe2718dc0a3208602adb_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10260,"brandName":"Swarovski","type":0,"logoUrl":"https://du.hupucdn.com/news_byte29555byte_630db5e96d66e6f5287c293cd78caf27_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10010,"brandName":"PRADA","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21018byte_f70b725f896e7d48d7cf5de27efb693a_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10107,"brandName":"UNIQLO","type":0,"logoUrl":"https://du.hupucdn.com/news_byte22384byte_3363df740785c4f46ff7e9e60732d44c_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10173,"brandName":"HIPANDA","type":0,"logoUrl":"https://du.hupucdn.com/news_byte30445byte_c66a18c65a8fed91a6790c51b4742f5a_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10219,"brandName":"HUMAN MADE","type":0,"logoUrl":"https://du.hupucdn.com/news_byte37800byte_decdf76555f22cb831ac23e08ab2018b_w150h150.jpg"},"seriesList":[]},{"brand":{"goodsBrandId":10348,"brandName":"PINKO","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21540byte_a15095f6f394d948ae5ab220d8d1a122_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10349,"brandName":"ISSEY MIYAKE","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21345byte_f151d2b6a79e5f9189d3edeb5febd68d_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10094,"brandName":"HERON PRESTON","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21445byte_263c6af2c24fe8eb020f2fad8956aae6_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10217,"brandName":"HARSH AND CRUEL","type":0,"logoUrl":"https://du.hupucdn.com/news_byte27648byte_68693ca8aa0d93a7bc4efacf7131a1d0_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10229,"brandName":"COACH","type":0,"logoUrl":"https://du.hupucdn.com/news_byte22573byte_2d963bacc8403d3bff0f44edd04dab64_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10230,"brandName":"MICHAEL KORS","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21530byte_ae96688098a3d529824fa5cb71bf3765_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10273,"brandName":"XLARGE","type":0,"logoUrl":"https://du.hupucdn.com/news_byte38276byte_061c84c498eadd44eb11704a5420f785_w688h628.jpg"},"seriesList":[]},{"brand":{"goodsBrandId":10012,"brandName":"Balenciaga","type":0,"logoUrl":"https://du.hupucdn.com/news_byte25051byte_c9098ab23afe7e5b2ebbe5bbe02cf20b_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10097,"brandName":"New Era","type":0,"logoUrl":"https://du.hupucdn.com/news_byte12037byte_2650d81fe891a08f41ba8ef58f92e4c8_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10236,"brandName":"UNDER GARDEN","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21683byte_ebeac156f070e9f48e74e13567a908ad_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10216,"brandName":"Suamoment","type":0,"logoUrl":"https://du.hupucdn.com/news_byte26349byte_999d4032e637fbccca3aaf6db95ef2ea_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":8,"brandName":"Asics","type":0,"logoUrl":"https://du.hupucdn.com/news_byte3352byte_31e3a9553fef833c3004a84c4c016093_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10261,"brandName":"TIFFANY & CO.","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21293byte_6af55972221b24da968a1b9957080c1e_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10045,"brandName":"CHANEL","type":0,"logoUrl":"https://du.hupucdn.com/news_byte32784byte_b947def32e782d20594230896ad2b342_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10302,"brandName":"alexander wang","type":0,"logoUrl":"https://du.hupucdn.com/news_byte20702byte_4635ead9077fefadaf9875638452a339_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10347,"brandName":"MLB","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21412byte_ba8096a44748f1e896828a6d1196f571_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10191,"brandName":"BEASTER","type":0,"logoUrl":"https://du.hupucdn.com/news_byte23781byte_319f230d9345cd5154b908631d2bb868_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10245,"brandName":"izzue","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21393byte_cf5140071b8824d433f4b32a51d49220_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10257,"brandName":"FIVE CM","type":0,"logoUrl":"https://du.hupucdn.com/news_byte22092byte_3cd80b1e49ad6bd28e5e371327424532_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10262,"brandName":"Acne Studios","type":0,"logoUrl":"https://du.hupucdn.com/news_byte26766byte_8e0cc00c1fccd1958d56b008370107cc_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":4984,"brandName":"得物","type":0,"logoUrl":"https://du.hupucdn.com/news_byte1528byte_5fd1d0d6bd3ff23d2b6c0d2933da1b8e_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10235,"brandName":":CHOCOOLATE","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21808byte_2418d1805f60850c961c31ea40982ed2_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10096,"brandName":"PALM ANGELS","type":0,"logoUrl":"https://du.hupucdn.com/news_byte22102byte_3d85af8f2d0566d7a1620404f9432be5_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":1302,"brandName":"WTAPS","type":0,"logoUrl":"https://du.hupucdn.com/news_byte5814byte_ce947464a6105c6aef7d7fb981aaa61e_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":4983,"brandName":"NEIGHBORHOOD","type":0,"logoUrl":"https://du.hupucdn.com/news_byte3804byte_316eb37426516d3cf8252fcbab6aa0cf_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10024,"brandName":"BANDAI","type":0,"logoUrl":"https://du.hupucdn.com/news_byte41491byte_d575b1bce5ab5754ea2444c0bb415782_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":2389,"brandName":"LEGO","type":0,"logoUrl":"https://du.hupucdn.com/news_byte33157byte_7e92ea9e2640626b9d52ce2a9fd2a75c_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10224,"brandName":"DANGEROUSPEOPLE","type":0,"logoUrl":"https://du.hupucdn.com/news_byte27331byte_fd65dfa6630e179a1bed93573a9b32cb_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10241,"brandName":"Acupuncture","type":0,"logoUrl":"https://du.hupucdn.com/news_byte26897byte_26ec3a3b2f532353a635cff0752eb743_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10255,"brandName":"MITARBEITER（IN）","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21741byte_058a1342e063fbb9fd341a1f3aca48a6_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":1318,"brandName":"FILA","type":0,"logoUrl":"https://du.hupucdn.com/news_byte24479byte_79cb074cf3d73a420d75a435aee91fe2_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10315,"brandName":"SANKUANZ","type":0,"logoUrl":"https://du.hupucdn.com/news_byte23445byte_3e251bad0695be109b037d80b9908e2a_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10221,"brandName":"*EVAE+MOB","type":0,"logoUrl":"https://du.hupucdn.com/news_byte22561byte_e52e3571b938f7027d4ea5ce1c406cb8_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10226,"brandName":"BABAMA","type":0,"logoUrl":"https://du.hupucdn.com/news_byte23766byte_8a0dcd76a4e7032a66209f40d0b6ec85_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10228,"brandName":"OMTO","type":0,"logoUrl":"https://du.hupucdn.com/news_byte23242byte_06cc9e12bd4efdf4d1885c401c224e10_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10237,"brandName":"OMT","type":0,"logoUrl":"https://du.hupucdn.com/news_byte24518byte_6be637e798e477e8c2e9e7d502e59b25_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10244,"brandName":"VERAF CA","type":0,"logoUrl":"https://du.hupucdn.com/news_byte22401byte_7c150e55199eb32e12bb29f01ed6c801_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":34,"brandName":"安踏","type":0,"logoUrl":"https://du.hupucdn.com/news_byte925102byte_5d9ca8cebc2286d70ef66f4f4a8f2983_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10210,"brandName":"CDG","type":0,"logoUrl":"https://du.hupucdn.com/news_byte20964byte_54ad49c012c262b02805451b9462f481_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10369,"brandName":"× × DESIGN","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21649byte_f3502bde5ec295493f6b1ffff54fdad9_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10017,"brandName":"PLACES+FACES","type":0,"logoUrl":"https://du.hupucdn.com/news_byte22034byte_87c416321487ad3071b2e886690b6c83_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10020,"brandName":"VERSACE","type":0,"logoUrl":"https://du.hupucdn.com/news_byte17169byte_7a363914e3e65ddcab341f2088451861_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10022,"brandName":"LONGINES","type":0,"logoUrl":"https://du.hupucdn.com/news_byte3779byte_b43ce49900670dcd8855801cd4ecbc3e_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10029,"brandName":"McQ","type":0,"logoUrl":"https://du.hupucdn.com/news_byte20529byte_0a3c77e055b5ea67e5dd976e0ae15ef9_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10031,"brandName":"Alpha Industries","type":0,"logoUrl":"https://du.hupucdn.com/news_byte10726byte_a964cf670ceeb6e83dd7dc74670d2d0e_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10033,"brandName":"Hasbro","type":0,"logoUrl":"https://du.hupucdn.com/news_byte33084byte_6ee0b3af2fe9007bd43d7e43b2d9cbcd_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10048,"brandName":"Boy London","type":0,"logoUrl":"https://du.hupucdn.com/news_byte12032byte_dc8badd06954530bab52bee2dcd2281e_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10053,"brandName":"MOSCHINO","type":0,"logoUrl":"https://du.hupucdn.com/news_byte3922byte_e6fed7cc9d76aaed983119b1f6ea4da2_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10099,"brandName":"VEJA","type":0,"logoUrl":"https://du.hupucdn.com/news_byte27380byte_01358f743e3668ee4f860cc03c6cee71_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10105,"brandName":"GAON","type":0,"logoUrl":"https://du.hupucdn.com/news_byte24582byte_5dc995e735d926f10686a3b2e4f99ffe_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10110,"brandName":"EDCO","type":0,"logoUrl":"https://du.hupucdn.com/news_byte25568byte_4c07bb13aeb5e88d127f5f30b0582ed2_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10111,"brandName":"FYP","type":0,"logoUrl":"https://du.hupucdn.com/news_byte24609byte_694a64457745672bd4e7b657b6753993_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10125,"brandName":"OPPO","type":0,"logoUrl":"https://du.hupucdn.com/news_byte25629byte_7fb979a04f572beaa96b0583f4204748_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10130,"brandName":"Corade","type":0,"logoUrl":"https://du.hupucdn.com/news_byte5181byte_7a202830db26f4d93c565e2cc1e0af4d_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10132,"brandName":"MostwantedLab","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21748byte_4c88547590072659de8e0731fef96a4f_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10135,"brandName":"PRBLMS","type":0,"logoUrl":"https://du.hupucdn.com/news_byte22576byte_910768509dbfed23275fa7989753dffd_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10138,"brandName":"zippo","type":0,"logoUrl":"https://du.hupucdn.com/news_byte28711byte_8d40191080a1a21111d66ce2ee000e90_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10142,"brandName":"UNVESNO","type":0,"logoUrl":"https://du.hupucdn.com/news_byte2826byte_fdb1b1046cae382cfb60cac11f9b281d_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10150,"brandName":"vivo","type":0,"logoUrl":"https://du.hupucdn.com/news_byte26242byte_b829524880093cc2099d470299889c89_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10246,"brandName":"HOKA ONE ONE","type":0,"logoUrl":"https://du.hupucdn.com/news_byte26308byte_1e82701c70c29b871b630adb45dbebd3_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10247,"brandName":"KEEN","type":0,"logoUrl":"https://du.hupucdn.com/news_byte30591byte_670bf1d37ce8479f3fa09a55d28dcb93_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10002,"brandName":"Y-3","type":0,"logoUrl":"https://du.hupucdn.com/news_byte29394byte_2f32b853acb651e2831f8797fe29fbfa_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10267,"brandName":"LOCCITANE","type":0,"logoUrl":"https://du.hupucdn.com/news_byte25047byte_c8480c6f2b9a32fc3a54524146bd1165_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10013,"brandName":"Neil Barrett","type":0,"logoUrl":"https://du.hupucdn.com/news_byte3026byte_cdeab7bf75187f17fa8c069c9a3a051a_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10269,"brandName":"Charlotte Tilbury ","type":0,"logoUrl":"https://du.hupucdn.com/news_byte23124byte_0113ad2025780a77a7f5131571ecee54_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10014,"brandName":"KENZO","type":0,"logoUrl":"https://du.hupucdn.com/news_byte7359byte_c71c56a9aea36427f7bb106f18151548_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10270,"brandName":"BVLGARI","type":0,"logoUrl":"https://du.hupucdn.com/news_byte22644byte_9dfd426ffa4b796999f49447b6a67f13_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10271,"brandName":"Jo Malone London","type":0,"logoUrl":"https://du.hupucdn.com/news_byte22269byte_51fd61cb797b6c2bbf0c0b84981c0948_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10016,"brandName":"Vetements","type":0,"logoUrl":"https://du.hupucdn.com/news_byte24790byte_b66758a5ea903a5a005798f7d84d1498_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10274,"brandName":"GIORGIO ARMANI","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21786byte_2857737687e9338787e5121b81e2fe27_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10019,"brandName":"Givenchy","type":0,"logoUrl":"https://du.hupucdn.com/news_byte23368byte_51dcde3cd1f5ef90c5734249bcd17af0_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10275,"brandName":"GUERLAIN","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21952byte_b06c9655af8bbd85bbacd7905c856d99_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10276,"brandName":"Fresh","type":0,"logoUrl":"https://du.hupucdn.com/news_byte29422byte_c362cefc52c99839bbf299bef133e165_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10277,"brandName":"Clé de Peau Beauté","type":0,"logoUrl":"https://du.hupucdn.com/news_byte24675byte_c3c1c3b08d7926e82fd1681f920a955f_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10278,"brandName":"LANCOME","type":0,"logoUrl":"https://du.hupucdn.com/news_byte22324byte_41fe4c8042bfd4761df3cbde50eb1ab0_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10023,"brandName":"FENDI","type":0,"logoUrl":"https://du.hupucdn.com/news_byte3735byte_363b11ad1f4b34f6b165818fe14ded88_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10279,"brandName":"Kiehls","type":0,"logoUrl":"https://du.hupucdn.com/news_byte22486byte_39f44b549295514934db3bea8696551a_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10280,"brandName":"MAC","type":0,"logoUrl":"https://du.hupucdn.com/news_byte20822byte_0d14fc90e743b48c0d198505ac7acbbd_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10026,"brandName":"Yves Saint Laurent","type":0,"logoUrl":"https://du.hupucdn.com/news_byte29430byte_88593ab0095ed38806e07d4afd4889cf_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10282,"brandName":"LA MER","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21643byte_c2302d6ae27f2fa9569a224a49da3097_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10284,"brandName":"CLARINS","type":0,"logoUrl":"https://du.hupucdn.com/news_byte23308byte_a69c3dfc25e7a7c6400ffe44d8242a30_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10285,"brandName":"NARS","type":0,"logoUrl":"https://du.hupucdn.com/news_byte25821byte_311c624a310303b590d5d4c062f056ea_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10286,"brandName":"benefit","type":0,"logoUrl":"https://du.hupucdn.com/news_byte25499byte_f2dadfa1b21c81b9e659300bf07e8d37_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10287,"brandName":"GLAMGLOW","type":0,"logoUrl":"https://du.hupucdn.com/news_byte22830byte_eb7b37c9e623fc1b2ee13c291e1a29aa_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10288,"brandName":"Too Faced","type":0,"logoUrl":"https://du.hupucdn.com/news_byte22156byte_47dd9a1fe0969e1648e912ee16cbb844_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10289,"brandName":"URBAN DECAY","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21218byte_dc1d505013e356a3479ad5295b6f1e75_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10290,"brandName":"FOREO","type":0,"logoUrl":"https://du.hupucdn.com/news_byte20670byte_924d6ad6b63fda5c7dae0c77b6e55a3f_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10035,"brandName":"Dyson","type":0,"logoUrl":"https://du.hupucdn.com/news_byte28101byte_18fa7633c4e27f221c840813d784080f_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10291,"brandName":"Christian Louboutin","type":0,"logoUrl":"https://du.hupucdn.com/news_byte24594byte_d45524f35597ed91bbd7544f9e652172_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10293,"brandName":"xVESSEL","type":0,"logoUrl":"https://du.hupucdn.com/news_byte23132byte_cc28fa998fb6243eb71054f6c2135db9_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10044,"brandName":"TISSOT","type":0,"logoUrl":"https://du.hupucdn.com/news_byte31626byte_d4191837d926ec7bbd1e29c5fe46e595_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10300,"brandName":"PRIME 1 STUDIO","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21836byte_44d1b5dc422073743a3c11647a8409a3_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10047,"brandName":"MCM","type":0,"logoUrl":"https://du.hupucdn.com/news_byte50051byte_3ed4a130ff4dc02151428c3e50978942_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10310,"brandName":"acme de la vie","type":0,"logoUrl":"https://du.hupucdn.com/news_byte22262byte_a8a932aaedbab86b34249828b7ed32f8_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10311,"brandName":"BE@RBRICK","type":0,"logoUrl":"https://du.hupucdn.com/news_byte23466byte_2e8da4a1f054a8e4682594a45612814e_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10065,"brandName":"Timberland","type":0,"logoUrl":"https://du.hupucdn.com/news_byte25895byte_88b2058d896df08f73cd94a47d2310f2_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":1000018,"brandName":"RAF SIMONS","type":0,"logoUrl":"https://du.hupucdn.com/FkYorY5yQT4Q4E66tjPrzETZ7R-p"},"seriesList":[]},{"brand":{"goodsBrandId":10068,"brandName":"PANERAI","type":0,"logoUrl":"https://du.hupucdn.com/news_byte32912byte_36220760228f319bb75f52330c7e4b3e_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":1000020,"brandName":"正负零","type":0,"logoUrl":"https://du.hupucdn.com/FsrWiDmNZYaV1MjkRu0KMGU065zO"},"seriesList":[]},{"brand":{"goodsBrandId":10069,"brandName":"MIDO","type":0,"logoUrl":"https://du.hupucdn.com/news_byte26922byte_be1c2be794cb6d454620f4692647e268_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10070,"brandName":"Dupont","type":0,"logoUrl":"https://du.hupucdn.com/news_byte28213byte_3d762e61d0d0ab8dec7d7dd92fe1dc99_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10071,"brandName":"kindle","type":0,"logoUrl":"https://du.hupucdn.com/news_byte27862byte_be5d55c9c358e569b89fbf8e12fc20a4_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10331,"brandName":"WHY PLAY","type":0,"logoUrl":"https://du.hupucdn.com/news_byte28380byte_363531321a5e823c56cc2f933f3be497_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10078,"brandName":"Logitech","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21472byte_ce700f9b3ca84b7a4a5f308f82bae04e_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10341,"brandName":"anello","type":0,"logoUrl":"https://du.hupucdn.com/news_byte25573byte_8080b45548c4b17bc976f8797ff158d5_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":1000045,"brandName":"DMCkal","type":0,"logoUrl":"https://du.hupucdn.com/FtcBWuRAZXH8rxoRoJSQDhQID6sT"},"seriesList":[]},{"brand":{"goodsBrandId":10350,"brandName":"A-COLD-WALL*","type":0,"logoUrl":"https://du.hupucdn.com/news_byte17623byte_ebcbe70f089dabe23e93588dc6ac66a3_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10354,"brandName":"CONKLAB","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21404byte_7fb50713eb0f986354735b304d5be896_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10101,"brandName":"GENANX/闪电","type":0,"logoUrl":"https://du.hupucdn.com/news_byte33425byte_c27fb3124848c48aee19c85441352048_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10358,"brandName":"FOOT INDUSTRY","type":0,"logoUrl":"https://du.hupucdn.com/news_byte20338byte_4e3b752398bf7ff9e16d9fe37e4ecee9_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10360,"brandName":"BONELESS","type":0,"logoUrl":"https://du.hupucdn.com/news_byte17690byte_8c346bdce381e0cf63c76f187a4fe042_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10361,"brandName":"umamiism","type":0,"logoUrl":"https://du.hupucdn.com/news_byte22545byte_34df2f448a017f7fdb3e570606c241b9_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10362,"brandName":"华人青年","type":0,"logoUrl":"https://du.hupucdn.com/news_byte22601byte_f52dc5ab9f4452f97babc47821d24021_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10363,"brandName":"FUNKMASTERS","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21027byte_1576a0f677e9cacd8762be6db99d4c78_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":1000061,"brandName":"GUESS","type":0,"logoUrl":"https://du.hupucdn.com/Fi6tDRWTi5rnQiW-ZB5BB-FbPoZN"},"seriesList":[]},{"brand":{"goodsBrandId":1000062,"brandName":"Needles","type":0,"logoUrl":"https://du.hupucdn.com/FiwdfFP76yqpag1r50r1qVG-TXad"},"seriesList":[]},{"brand":{"goodsBrandId":10368,"brandName":"Subtle","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21987byte_4b242f882bf5df63b2da5eae632fa29c_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10116,"brandName":"EMPORIO ARMANI","type":0,"logoUrl":"https://du.hupucdn.com/news_byte22342byte_7060a8a9b7c6b335143673f5417a1944_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10124,"brandName":"AMONSTER","type":0,"logoUrl":"https://du.hupucdn.com/FjZYBGDKtsc_9n8ftq28XsMRxZxB"},"seriesList":[]},{"brand":{"goodsBrandId":10381,"brandName":"PCMY","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21692byte_205236932bf037dab9965dd2be87085e_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10127,"brandName":"Rothco","type":0,"logoUrl":"https://du.hupucdn.com/news_byte24098byte_12c50dcd1c1044fa4a6335bedd98e7d4_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10131,"brandName":"THE WIZ","type":0,"logoUrl":"https://du.hupucdn.com/news_byte6823byte_6a92589a3c42dcb6a1f3e849966daf53_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10388,"brandName":"TSMLXLT","type":0,"logoUrl":"https://du.hupucdn.com/news_byte20983byte_d18f9145f160a5dd3b5d0ca45acec510_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10390,"brandName":"TRICKCOO","type":0,"logoUrl":"https://du.hupucdn.com/news_byte25337byte_823a55d69768b65e728f896971a0185d_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10391,"brandName":"NOCAO","type":0,"logoUrl":"https://du.hupucdn.com/news_byte22420byte_91b1ed0e11d4948a817f5ae35a0bfd99_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10136,"brandName":"PROS BY CH","type":0,"logoUrl":"https://du.hupucdn.com/news_byte6186byte_323eba7633b20d61d566dbc0bdb83f13_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10137,"brandName":"OXY","type":0,"logoUrl":"https://du.hupucdn.com/news_byte24524byte_535ab7db658c3f1c8e00a821e5587585_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10394,"brandName":"FLOAT","type":0,"logoUrl":"https://du.hupucdn.com/news_byte25774byte_07be4b895302ee06cbd9ad53aa017ed5_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10143,"brandName":"Suicoke","type":0,"logoUrl":"https://du.hupucdn.com/news_byte22613byte_16cd0ea92dde2aea19b76b46491814bb_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10146,"brandName":"GARMIN","type":0,"logoUrl":"https://du.hupucdn.com/news_byte20845byte_5af278c31aad1b5e0982544840c2df96_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10151,"brandName":"BANPRESTO","type":0,"logoUrl":"https://du.hupucdn.com/news_byte56132byte_ee71a1bac952dac4cd3f59b4c6673203_w800h800.jpg"},"seriesList":[]},{"brand":{"goodsBrandId":10153,"brandName":"Harman/Kardon","type":0,"logoUrl":"https://du.hupucdn.com/news_byte17446byte_134385ee63bf9d12cd7f98e27344310e_w150h150.jpg"},"seriesList":[]},{"brand":{"goodsBrandId":10413,"brandName":"OSCill","type":0,"logoUrl":"https://du.hupucdn.com/news_byte23787byte_88a0a8c1b72cd8693957af2a53b89bd5_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10414,"brandName":"LIFEGOESON","type":0,"logoUrl":"https://du.hupucdn.com/FgHxeSwXg9SKBtRNrNNKjn-O8yxf"},"seriesList":[]},{"brand":{"goodsBrandId":10161,"brandName":"PSO Brand","type":0,"logoUrl":"https://du.hupucdn.com/news_byte47498byte_0bb2a47154dfa0fc914e98cfeae6c407_w1000h1000.jpg"},"seriesList":[]},{"brand":{"goodsBrandId":10167,"brandName":"EVISU","type":0,"logoUrl":"https://du.hupucdn.com/news_byte8745byte_0ba5f52e059d3e91803a05843c2b22e2_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10423,"brandName":"Maison Margiela","type":0,"logoUrl":"https://du.hupucdn.com/news_byte22857byte_d8df7145e944cd7b203d3f5520b06c43_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10168,"brandName":"INXX","type":0,"logoUrl":"https://du.hupucdn.com/news_byte20442byte_4c50ce6dca7408dec92df78b72106e46_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10169,"brandName":"B&O","type":0,"logoUrl":"https://du.hupucdn.com/news_byte36636byte_b32fd6036ba60c4f868b197ada8b8c6f_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10425,"brandName":"Charlie Luciano","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21051byte_28faf07c5d5a078a6fc18357413ce7c3_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10170,"brandName":"CITIZEN","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21252byte_1158debba23c31ccfed657aa8ce762bd_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10171,"brandName":"LOFREE","type":0,"logoUrl":"https://du.hupucdn.com/news_byte22408byte_1af23b04a9bc352bfff21edb63514d39_w150h150.jpg"},"seriesList":[]},{"brand":{"goodsBrandId":10429,"brandName":"Arcteryx","type":0,"logoUrl":"https://du.hupucdn.com/news_byte24934byte_5ebce6f644ee8ebdbc89f04a068fc1af_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10174,"brandName":"DAMTOYS","type":0,"logoUrl":"https://du.hupucdn.com/news_byte31687byte_84591020e1a16ce89318585a5d84e9fc_w150h150.jpg"},"seriesList":[]},{"brand":{"goodsBrandId":10175,"brandName":"POP MART","type":0,"logoUrl":"https://du.hupucdn.com/news_byte24981byte_909c5a578874dac97c6d3796be69cdf3_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10179,"brandName":"野兽王国","type":0,"logoUrl":"https://du.hupucdn.com/news_byte36849byte_5af274d0628f77ca06994e30ed50d5c4_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10183,"brandName":"ALIENWARE/外星人","type":0,"logoUrl":"https://du.hupucdn.com/news_byte25149byte_458a868f82f2ac201e5d2f56fc087d60_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10184,"brandName":"Herschel","type":0,"logoUrl":"https://du.hupucdn.com/news_byte34213byte_403f7a96cd33f1cfdb12769a7e870f65_w824h752.png"},"seriesList":[]},{"brand":{"goodsBrandId":10187,"brandName":"科大讯飞","type":0,"logoUrl":"https://du.hupucdn.com/news_byte25000byte_8351390b01275c1fcaa8f20a040b6dfe_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10443,"brandName":"chinism","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21910byte_d24daabd4b84bba6c37e22a42dd18602_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10188,"brandName":"韶音","type":0,"logoUrl":"https://du.hupucdn.com/news_byte6089byte_b5d736ec8a0c1269eceb94dcfa520c37_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10190,"brandName":"SAINT LAURENT","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21416byte_6836702d9d6f487e44b8922d8eaeb86b_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10193,"brandName":"SPALDING","type":0,"logoUrl":"https://du.hupucdn.com/news_byte27011byte_12f13f15a9a198939f3d9b847dbdb214_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10195,"brandName":"Levis","type":0,"logoUrl":"https://du.hupucdn.com/news_byte23207byte_ad584d3079f341b83325f4974b99e342_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10196,"brandName":"SENNHEISER","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21466byte_f597724d3c9eb3294441c608cb59e1fe_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10197,"brandName":"CASETIFY","type":0,"logoUrl":"https://du.hupucdn.com/news_byte23539byte_3a85a808033ed920a29cac5fad902b6f_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10199,"brandName":"JMGO","type":0,"logoUrl":"https://du.hupucdn.com/news_byte26989byte_cdd8e059931aa405f55c5d2426862a6b_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10200,"brandName":"PHILIPS","type":0,"logoUrl":"https://du.hupucdn.com/news_byte24239byte_5655ed4f287863630934c96aa823346a_w150h150.jpg"},"seriesList":[]},{"brand":{"goodsBrandId":10201,"brandName":"SEIKO","type":0,"logoUrl":"https://du.hupucdn.com/news_byte22717byte_6bfa41469825cfd6c70f5e3080d5de6a_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10202,"brandName":"GENANX","type":0,"logoUrl":"https://du.hupucdn.com/news_byte9514byte_77dee80e931dfd8b528f609c400951e4_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10204,"brandName":"TIANC","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21593byte_aa160ed7e50ca090d629490010346a9a_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10205,"brandName":"Drew House","type":0,"logoUrl":"https://du.hupucdn.com/news_byte30015byte_31ba151ba30e01ae6132ce9584b4e49a_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10206,"brandName":"小米/MI","type":0,"logoUrl":"https://du.hupucdn.com/news_byte23786byte_d04434a4af3b56e20758cbeaed4f4531_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10207,"brandName":"CALVIN KLEIN","type":0,"logoUrl":"https://du.hupucdn.com/news_byte24775byte_736593d1ee0995be050b1fbcec77bf46_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":2016,"brandName":"DanielWellington","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21711byte_f48145a65169f913b0139ff2e1811e78_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10211,"brandName":"飞智","type":0,"logoUrl":"https://du.hupucdn.com/news_byte26616byte_8001c14855f8528d7bccc31183bfaf75_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10213,"brandName":"TOM FORD","type":0,"logoUrl":"https://du.hupucdn.com/news_byte21248byte_2994883ac1627497e75e9b99ba327c48_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10485,"brandName":"RickyisClown","type":0,"logoUrl":"https://du.hupucdn.com/news_byte22583byte_98f823c8acb1459e6c72f5bdaf8a88b0_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10233,"brandName":"Dr.Martens","type":0,"logoUrl":"https://du.hupucdn.com/news_byte31892byte_8d31e2f10cc7fffe8d99545d757dfff6_w150h150.png"},"seriesList":[]},{"brand":{"goodsBrandId":10238,"brandName":"APPortfolio","type":0,"logoUrl":"https://du.hupucdn.com/news_byte30968byte_19dd10185fc4b82037621b3708a613e4_w150h150.png"},"seriesList":[]}]},"status":200}
        super(DuGet, self).__init__()

    def sign(self, raw_sign_code_str):
        # md5原始sign的字符串
        m = hashlib.md5()
        m.update(raw_sign_code_str.encode("utf8"))
        return m.hexdigest()

    def search_keywords(self, keywords, sortMode=1, sortType=1, page=0):
        # 关键词搜索商品接口
        sign = self.sign('limit20page{}showHot-1sortMode{}sortType{}title{}unionId19bc545a393a25177083d4a748807cc0'.format(page, sortMode, sortType, keywords))
        url = 'https://app.poizon.com/api/v1/h5/search/fire/search/list'
        params = {
            'sign': sign,
            'title': quote(keywords),
            'page': page,
            'sortType': sortType,
            'sortMode': sortMode,
            'limit': '20',
            'showHot': '-1',
            'unionId': ''
        }

        soldNum = -1
        price = 0
        others = []
        try:
            if get_proxy():
                res_data = requests.get(url, headers=self.headers, params=params, timeout=5, proxies=get_proxy()).json()
            else:
                res_data = requests.get(url, headers=self.headers, params=params, timeout=5).json()
            if res_data['data']['total'] == 1:
                it = res_data['data']['productList'][0]
                soldNum = it.get('soldNum', -1)
                price = it.get('price', 0)
                if price > 0:
                    price = price / 100
            elif res_data['data']['total'] > 1 and res_data['data']['total'] < 5:
                for it in res_data['data']['productList']:
                    others.append({"soldNum":it.get('soldNum'), "price":it.get('price'), "title":it.get('title')})
        except Exception as e:
            logger.error("{}:{} {} {}".format(self.__class__, url, keywords, e))
        return soldNum, price, json.dumps(others)

    def show(self):
        # d = DuGet()
        # res = d.search_keywords('fw9348', 1, 1)
        # if res['data']['total'] == 1:
        #     data_info = res['data']['productList'][0]
        #     print("soldNum:{},price:{},minPrice:{},spuMinPrice:{},{},{}:{}".format(data_info.get('soldNum', '异常'), data_info.get('price', '异常'),
        #            data_info.get('minSalePrice', '异常'), data_info.get('spuMinSalePrice', '异常'),
        #            data_info.get('articleNumber', '异常'), data_info.get('title', '异常'), data_info.get('subTitle', '异常')))
        pass

    def run(self):
        logger.info("start thread {}".format(self.__class__))
        statistic_count = 0
        while True:
            if self.task_queue.empty():
                time.sleep(1)
                continue
            items = self.task_queue.get()
            db_id, good_id = items[0], items[1]
            soldNum, price, others = self.search_keywords(good_id)
            self.results_queue.put((db_id, soldNum, price, others))
            statistic_count += 1
            if statistic_count % 100 == 0:
                logger.info("{} done {}, current {}:{}".format(self.__class__, statistic_count,
                                                               self.task_queue.qsize(), self.results_queue.qsize()))
            time.sleep(random.uniform(0, self.sleep))


class MailNotify(threading.Thread):
    def __init__(self, _dbhost, _dbport, _dbuser, _dbpwd, _db, _mail_host, _mailport, _mail_pass,
                 _sender, _receivers, _params, _sleep=30):
        self.dbhost = _dbhost
        self.dbport = _dbport
        self.dbuser = _dbuser
        self.dbpwd = _dbpwd
        self.db = _db
        self.mail_host = _mail_host
        self.mail_port = _mailport
        self.mail_pass = _mail_pass
        self.sender = _sender
        self.receivers = _receivers
        self.params = _params

        self.last_list = set()
        self.lowprice_last_list = set()
        self.last_discount_list = set()
        self.sleep = _sleep
        self.sql = SqlModel(_dbhost, _dbport, _dbuser, _dbpwd, _db)

        super(MailNotify, self).__init__()

    def send(self, send_list, header=None):
        send_str_list = []
        for it in send_list:
            tmp_str = """<p>name: {},id: {} delta:{},price:{}/{}({}),du:{}/{},extern:{},new:{},sold:{} <a href={}>{}</a>
            <a href={}>(详情)</a></p>""".format(it['source'],it['good_id'],it['delta'],
                                                it['price'],it['marketPrice'],it['saleDiscount'],
                                                it['du_price'],it['du_count'],it['source_extern'],
                                                it.get('new', 0),
                                                it['sold_items'],it['pic'],it['title'],it['detail'])
            send_str_list.append(tmp_str)
        if header:
            contents = "<h3>{}</h3>".format(header) + ''.join(send_str_list)
        else:
            contents = ''.join(send_str_list)
        message = MIMEText(contents, 'html', 'utf-8')

        message['From'] = Header("GoodsInfo", 'utf-8')
        message['To'] = Header("Receiver", 'utf-8')

        subject = 'Goods Info'
        message['Subject'] = Header(subject, 'utf-8')

        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, self.mail_port)
            smtpObj.login(self.sender, self.mail_pass)
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            smtpObj.quit()
        except smtplib.SMTPException as e:
            logger.error('send {} mail error {}'.format(self.receivers, e))
        else:
            logger.info("send {} email success".format(self.receivers))

    def get_list(self, price_delta, count_delta, limit=0, size=50):
        now_day = datetime.datetime.now().strftime('%Y-%m-%d')
        sql = 'select title,good_id,saleDiscount,detail,pic,price,du_price,marketPrice,du_count,source_extern,' \
              '`source`,extern,sold_items,updated_date,updated_day from tb_goods ' \
              'where du_price-price>=%s and du_count>%s and updated_day=%s order by updated_ts desc limit %s,%s'
        res = self.sql.execute(sql, [price_delta, count_delta, now_day, limit, size])
        for d in res:
            d['delta'] = d['du_price'] - d['price']
        return res

    def get_discount_list(self, max_discount, min_marketPrice, limit=0, size=50):
        now_day = datetime.datetime.now().strftime('%Y-%m-%d')
        sql = 'select title,good_id,saleDiscount,discount,detail,pic,price,du_price,marketPrice,du_count,source_extern,' \
              '`source`,extern,sold_items,updated_date,updated_day from tb_goods ' \
              'where discount<%s and marketPrice>%s and updated_day=%s order by updated_ts desc limit %s,%s'
        res = self.sql.execute(sql, [max_discount, min_marketPrice, now_day, limit, size])
        for d in res:
            d['delta'] = d['du_price'] - d['price']
        res.sort(key=lambda x:x['discount'], reverse=False)
        return res

    def run(self):
        logger.info("start thread {}".format(self.__class__))
        now_day = datetime.datetime.now().strftime("%Y-%m-%d")
        while True:
            res = self.get_list(self.params.get('delta', 50), self.params.get('delta_count', 500), size=200)
            is_send = False
            for it in res:
                tmp_key = "{}_{}".format(it['good_id'], it['price'])
                if tmp_key not in self.last_list:
                    self.last_list.add(tmp_key)
                    it['new'] = 1
                    is_send = True
            if is_send:
                res.sort(key=lambda x: (x.get('new', 0), x['delta']), reverse=True)
                self.send(res[:100])

            # res = self.get_list(self.params.get('lowprice_delta', 200), self.params.get('lowprice_delta_count', 50), size=200)
            # is_send = False
            # for it in res:
            #     tmp_key = "{}_{}".format(it['good_id'], it['price'])
            #     if tmp_key not in self.lowprice_last_list:
            #         self.lowprice_last_list.add(tmp_key)
            #         it['new'] = 1
            #         is_send = True
            # if is_send:
            #     res.sort(key=lambda x: (x.get('new', 0), x['delta']), reverse=True)
            #     self.send(res[:100], 'lowprice')

            # res = self.get_discount_list(self.params.get('discount', 3), self.params.get('discount_count', 500))
            # is_send = False
            # for it in res:
            #     tmp_key = "{}_{}".format(it['good_id'], it['price'])
            #     if tmp_key not in self.last_discount_list:
            #         self.last_discount_list.add(tmp_key)
            #         it['new'] = 1
            #         is_send = True
            # if is_send:
            #     self.send(res, 'discount')

            time.sleep(self.sleep)
            if now_day != datetime.datetime.now().strftime("%Y-%m-%d"):
                self.last_list = set()
                self.lowprice_last_list = set()
                now_day = datetime.datetime.now().strftime("%Y-%m-%d")


class BaseGet(threading.Thread):
    def __init__(self, _dbhost, _dbport, _dbuser, _dbpwd, _db):
        self.dbhost = _dbhost
        self.dbport = _dbport
        self.dbuser = _dbuser
        self.dbpwd = _dbpwd
        self.cookies = None
        self.api_key = None
        self.db = _db
        self.sql = SqlModel(_dbhost, _dbport, _dbuser, _dbpwd, _db)
        super(BaseGet, self).__init__()

    def init(self):
        cookies, api_key = self.get_cookie()
        if not cookies:
            return False
        self.cookies = cookies
        self.api_key = api_key
        return True

    def get_headers(self):
        return {
            "user-agent": random.choice(user_agent_list),
            "referer": "https://list.vip.com/"
        }

    def get_detail_url(self, brandId, productId):
        return "https://detail.vip.com/detail-{}-{}.html".format(brandId, productId)

    @staticmethod
    def get_discount(dis_str):
        if not dis_str:
            return 9999
        dis_str = dis_str.strip('\r\n ')
        res = dis_str.replace('折', '').replace('起', '')
        try:
            return float(res)
        except Exception as e:
            logger.error("{} {}".format(dis_str, e))
        return 9999

    def get_cookie(self):
        results = {}
        url = 'https://www.vip.com/'
        # res = requests.get(url, headers=self.headers)
        res = self.get(url, headers=self.get_headers())
        if not res:
            return None, None
        for cookie in res.cookies:
            results[cookie.name] = cookie.value
        results['mars_cid'] = '1604906927034_08fa7a00d3c9cd0288978fe43e69bb46'

        url = 'https://shop.vipstatic.com/js/public/core3.1.0-hash-1a0a48d2.js'
        params = {
            "2017111202": ""
        }

        api_key = ''
        try:
            res = self.get(url, headers=self.get_headers(), params=params)
            re_result = re.search(r'(?<=(api_key:)).*(?=(",))', res.text)
            api_key = re_result.group().strip('\r\n ')
            if api_key.startswith('"'):
                api_key = api_key[1:]
        except Exception as e:
            logger.error("{}:{} {}".format(self.__class__, url, e))
        return results, api_key

    def get(self, url, headers=None, params=None, cookies=None):
        for _ in range(3):
            try:
                if get_proxy():
                    return requests.get(url, headers=headers, params=params, cookies=cookies, timeout=5, proxies=get_proxy())
                return requests.get(url, headers=headers, params=params, cookies=cookies, timeout=5)
            except Exception as e:
                logger.error("{} {}".format(url, e))
                time.sleep(random.uniform(0, 3))

    def save(self, datas):
        self.sql.add_goods(datas)


class VipGet(BaseGet):
    def __init__(self, pro_dict, dbhost, dbport, dbuser, dbpwd, db):
        self.products_dict = pro_dict
        'https://mapi.vip.com/vips-mobile/rest/shopping/pc/product/module/list/v2'
        """
            callback: getMerchandiseDroplets1
            app_name: shop_pc
            app_version: 4.0
            warehouse: VIP_SH
            fdc_area_id: 103101101
            client: pc
            mobile_platform: 1
            province_id: 103101
            api_key: 70f71280d5d547b2a7bb370a529aeea1
            user_id: 
            mars_cid: 1604906927034_08fa7a00d3c9cd0288978fe43e69bb46
            wap_consumer: a
            productIds: 6917911362416874258,6918272259348416466,6917911257618883282,6917911275714884626,6918272259314735058,6918909834458755282,6917911433835865106,6919021632876781780,6918503984356577618,6918402604659680662,6919021632893587668,6918272259331573714,6917911272754524882,6918453328428094290,6918453328394470226,6918899417785542042,6918970532806683476,6917911361743111058,6918503984322965842,6918931757022714260,6919002736727304026,6917911394618037330,6918931757005846932,6918503984289370450,6919002736693610330,6917937443256488852,6918979686875607378,6918979686825087314,6917911264935498898,6918503984356569426,6918503984339771730,6918383405679720338,6917911240705196306,6919002736727344986,6918705969115694162,6918909834408227026,6918931757106878868,6918702423760200786,6918979686841954642,6918979686825079122,6918931757005916564,6918979686858752338,6918702423743374418,6918979686892446034,6918503984238920018,6918402604693517718,6918979686825095506,6918702423760241746,6918535739428810898,6918103940592551570
            scene: brand
            standby_id: nature
            extParams: {"multiBrandStore":"","stdSizeVids":"","subjectId":"","brandId":"","preheatTipsVer":"3","couponVer":"v2","exclusivePrice":"1","iconSpec":"2x"}
            context: 
            _: 1604907079000
        """
        super(VipGet, self).__init__(dbhost, dbport, dbuser, dbpwd, db)

    def get_product_ids(self, product_type):
        results_list = []
        for i in range(1, 80):
            url = "https://list.vip.com/api-ajax.php"
            params = {
                "callback": "getMerchandiseIds",
                "getPart": "getMerchandiseRankList",
                "fromIndex": "0",
                "mInfoNum": "0",
                "batchSize": "0",
                "r": "{}".format(product_type),
                "q": "|0||0|0|{}".format(i),
                "brandStoreSns": "",
                "vipService": "",
                "props": "",
                "landingOption": "",
                "preview": "0",
                "sell_time_from":"",
                "time_from":"",
                "token":"",
                "_": "{}".format(int(time.time()) * 1000)
            }
            try:
                res = self.get(url, headers=self.get_headers(), params=params)
                if res.text.startswith('getMerchandiseIds('):
                    res = json.loads(res.text[len('getMerchandiseIds('):-1])
                    results_list.extend(res['data']['getMerchandiseRankList']['products'])
                    logger.info("get ids {}:{}".format(self.products_dict[product_type], len(results_list)))
            except Exception as e:
                logger.error("{}:{} {}".format(url, i, e))
                break
            else:
                time.sleep(random.uniform(0, 3))

        return results_list

    def get_products(self, product_type):
        product_ids = self.get_product_ids(product_type)
        logger.info("{} products:{}".format(self.products_dict[product_type], len(product_ids)))

        ts = int(time.time()) * 1000
        url = 'https://mapi.vip.com/vips-mobile/rest/shopping/pc/product/module/list/v2'

        for i_index in range(10000):
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
                                           self.products_dict[product_type], 0, 0, json.dumps({}), int(time.time()),
                                           datetime.datetime.now(), datetime.datetime.now().strftime("%Y-%m-%d")
                                           ))
            except Exception as e:
                logger.error("{}:{}:{}".format(self.__class__, url, e))

            if products_infos:
                self.save(products_infos)
                logger.info("add {} {}".format(self.products_dict[product_type], len(products_infos)))
            time.sleep(random.uniform(0, 3))

    def run(self):
        while True:
            res = self.init()
            if not res:
                time.sleep(2)
            else:
                break

        while True:
            for k, v in self.products_dict.items():
                self.get_products(k)
            time.sleep(1)


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
    goods_dict = {
        '100782909': 'nike',
        '100781965': 'nike_sport',
        '100782915': 'vans',
        '100782928': 'adidas',
        '100707713': 'adidas_neo',
        '100782923': 'adidas_sport',
        '100781402': 'puma',
        '100796138': 'puma_sport',
        '100782927': 'converse',
        '100782922': 'skechers',
        '100782924': 'jordan',
        '100787685': 'skechers_sport',
        '100782939': 'new_balance',
        '100786078': 'new_balance_sport',
        '100782926': 'fila',
        '100782919': 'timberland',
        '100782911': '北面',
        '100782929': '鬼冢虎',
        '100782903': 'under_armour',
        '100707710': '卡西欧CASIO腕表',
        '100707659': 'COACH箱包',
        '100782940': 'Champion',
        '100707702': '浪琴LONGINES腕表',
        '100707644': '天梭TISSOT腕表',
        '100707676': 'VERSUS石英表'
    }

    search_list = [
        'ah2613',
        'coach男包',
        'coach女包',
        'coach女鞋子',
        'coachT恤',
        'coach短袖',
        'coach',
        'armani外套',
        'armaniT恤',
        'armani短袖',
        'armani女装',
        'armani男装',
        'armani',
        'burberry围巾',
        'burberry包',
        'burberryT恤',
        'burberry短袖',
        'burberry',
        'gucci女包',
        'gucci',
        'michael kors女士',
        'michael kors女士包手提',
        'michael kors男士',
        'michael kors',
        'chanel香水',
        'chanel口红',
        'chanel',
        'mcm双肩包',
        'mcm单肩包',
        'mcm',
        'dior口红',
        'dior香水',
        'dior',
        'unifree女装',
        'unifree',
        'dior',
        'hermes香水',
        'hermes',
        'apm',
        'swarovski项链',
        'swarovski',
        'mlb',
        'genanx',
        'gentlemonster太阳镜',
        'gentlemonster墨镜',
        'gentlemonster',
        'chanel',
        'martens',
        'timberland',
        'timberlandT恤',
        'timberland短袖',
        'timberland男鞋',
        'timberland女鞋',
        '欧文',
        'adidas三叶草',
        'fila',
        'filaT恤',
        'fila短袖',
        'fila女鞋',
        'fila男鞋',
        'adidas羽绒服',
        '三叶草羽绒服',
        'fila羽绒服'
        'adidas三叶草裤子',
        '北面羽绒服',
        '北面',
        'champion',
        'championT恤',
        'champion短袖',
        'champion羽绒服',
        'adidas三叶草卫衣',
        'adidas羽绒服',
        'adidas篮球',
        'adidas足球',
        'adidas卫衣男',
        'adidas卫衣女',
        'adidasT恤',
        'adidas短袖',
        '詹姆斯',
        'boost',
        '空军一号',
        'nike羽绒服',
        'puma羽绒服',
        'nike男鞋',
        'puma男鞋',
        'puma卫衣男',
        'puma卫衣女',
        'nike女鞋',
        'puma女鞋',
        'nike卫衣',
        'nike短袖',
        'nikeT恤',
        'nike裤子',
        'nike篮球',
        'nike足球',
        '李宁闪击',
        '李宁音速',
        '李宁驭帅',
        '李宁韦德之道',
        '李宁篮球',
        '李宁足球',
        '李宁T恤',
        '李宁短袖',
        'adidas',
        'zoom',
        '三叶草羽绒服',
        'm2k',
        '李宁',
        '李宁卫衣男',
        '李宁卫衣女',
        '李宁裤子',
        '李宁羽绒服',
        'vans 板鞋',
        '皮克',
        '皮克卫衣男',
        '皮克卫衣女',
        '皮克男鞋',
        '皮克女鞋',
        '皮克T恤',
        '皮克短袖',
        '皮克羽绒服',
        'air jordan',
        'air force',
        '1970s',
        'dunk sb',
        'newbalance',
        'newbalance羽绒服',
        '哥伦比亚',
        '哥伦比亚羽绒服',
        'anta',
        'anta羽绒服',
        'anta女鞋',
        'anta男鞋',
        'antaT恤',
        'anta短袖',
        'kappa羽绒服',
        'kappa',
        '锐步运动鞋男',
        '锐步运动鞋女',
        '锐步卫衣',
        '锐步T恤',
        '锐步短袖',
        '锐步',
        '361男鞋',
        '361女鞋',
        '361卫衣',
        '361T恤',
        '361短袖',
        '361',
    ]

    works = []
    tasks_detail = Queue(1000)
    results_detail = Queue(1000)
    tasks_du = Queue(1000)
    results_du = Queue(1000)
    dbhost = '127.0.0.1'
    dbport = 3306
    dbuser = 'test'
    dbpwd = 'test'
    db = 'goods'
    mailhost = 'smtp.qq.com'
    mailport = 465
    mailpwd = ''
    mailsender = '798990255@qq.com'
    mailreceivers = ['798990255@qq.com', '1589569837@qq.com']

    vip = VipGet(goods_dict, dbhost, dbport, dbuser, dbpwd, db)
    works.append(vip)

    update_result = UpdateResults(results_detail, results_du, dbhost, dbport, dbuser, dbpwd, db)
    works.append(update_result)

    generator_task = GeneratorTask(tasks_detail, tasks_du, dbhost, dbport, dbuser, dbpwd, db)
    works.append(generator_task)

    params = {
        "delta": 60,
        "delta_count": 100,
        "discount": 3,
        "discount_count": 100,
        "lowprice_delta": 100,
        "lowprice_delta_count": 100
    }
    mail_task = MailNotify(dbhost, dbport, dbuser, dbpwd, db, mailhost, mailport, mailpwd, mailsender, mailreceivers, params)
    works.append(mail_task)

    search_vip = SearchVIPGet(search_list, dbhost, dbport, dbuser, dbpwd, db)
    works.append(search_vip)

    for _ in range(4):
        d = DuGet(tasks_du, results_du)
        works.append(d)

    for _ in range(4):
        d = GoodDetailGet(tasks_detail, results_detail)
        works.append(d)

    for it in works:
        it.start()

    for it in works:
        it.join()
    logger.log("结束!!")




