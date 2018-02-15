# coding=utf-8
import MySQLdb
from settings import *
import time


connection = MySQLdb.Connect(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    passwd=MYSQL_PASSWORD,
    db=MYSQL_DATABASE,
)
cur = connection.cursor()


class UrlSql(object):
    def __init__(self, urls=None):
        self.conn = connection
        self.cur = cur
        self.query = []
        self.start_time = time.time()
        if urls is not None:
            self.urls = urls
        else:
            self.urls = []

    def insert_url_into_database(self, url=None):
        """向数据库插入数据"""
        try:
            sql = 'INSERT INTO crawled_url_list(`url`) VALUES (%(url)s)'
            if url is None:
                for img_url in self.urls:
                    value = {
                        'url': img_url,
                    }
                    self.cur.execute(sql, value)
                    self.conn.commit()
            else:
                value = {
                    'url': url,
                }
                self.cur.execute(sql, value)
                self.conn.commit()
            print u'数据导入成功\n'
        except MySQLdb.MySQLError as e:
            self.conn.rollback()
            print e
            print u'数据导入失败'

    def get_url_from_database(self):
        """从数据库获取数据"""
        try:
            sql = 'SELECT `url` from crawled_url_list'
            self.cur.execute(sql)
            ret = self.cur.fetchall()

            for url in ret:
                self.query.append(url[0])
        except MySQLdb.MySQLError as e:
            print(e)

    def delete_all_data(self):
        """删除所有数据"""
        try:
            sql = 'DELETE FROM crawled_url_list WHERE `URL` IS NOT NULL'
            self.cur.execute(sql)
            sel = raw_input('正在删除数据库所有数据, 请确认(y/n)')[0]
            if sel == 'y':
                self.conn.commit()
                print u'<<<<<<<<数据已删除!<<<<<<<<'
            elif sel == 'n':
                print u'<<<<<<<操作正在取消<<<<<<<<'
        except MySQLdb.MySQLError as e:
            self.conn.rollback()
            print e

    def exit(self):
        """退出方法"""
        self.cur.close()
        self.conn.close()
        print u'>>>>>>>>>数据库连接已断开<<<<<<<<<'
        print u'程序运行时间: {:.6f} (s)'.format(time.time()-self.start_time)
        print u'>>>>结束时间:\n' + time.ctime()
        print u'>>>>>>>>程序即将退出<<<<<<<<\n'
        time.sleep(4)
        print u'>>>>>>>>程序已退出<<<<<<<<<'