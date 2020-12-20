import time
import logging
import pymysql
from pymysql.cursors import DictCursor
from DBUtils.PersistentDB import PersistentDB

logger = logging.getLogger(__file__)


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
            sql = 'insert into tb_guanwang(uuid,productId,good_id,title,pic,detail,discount,price,fullPrice,' \
                  'salesChannel,source,du_price,du_count,extern,sold_items,updated_ts,updated_date,updated_day) ' \
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



