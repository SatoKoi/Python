# -*- coding:utf-8 -*-
import pymysql
from .. import settings
from scrapy.log import logger

__author__ = 'KoiSato'

connection = pymysql.connect(
    host=settings.MYSQL_HOST,
    port=settings.MYSQL_PORT,
    user=settings.MYSQL_USER,
    passwd=settings.MYSQL_PWD,
    db=settings.MYSQL_DATABASE,
    charset=settings.MYSQL_CHARSET
)

cur = connection.cursor()


class Sql(object):
    """Sql类"""

    @classmethod
    def insert_message(cls, *args, flag=None):
        """插入数据
        :param args: 所有位置参数以包含在一个元组里的方式传入"""
        if flag == 1:
            sql = "INSERT INTO `笔趣阁` VALUES (%(name)s, %(author)s, %(category)s, %(status)s, %(url)s, %(id)s)"
            value = {
                'name': args[0],
                'author': args[1],
                'category': args[2],
                'status': args[3],
                'url': args[4],
                'id': args[5]
            }
        elif flag == 2:
            sql = """INSERT INTO `笔趣阁章节内容` VALUES (%(book_name)s, %(book_id)s, %(chapter_name)s, %(chapter_id)s, %(chapter_url)s,
                  %(chapter_content)s)"""
            value = {
                'book_name': args[0],
                'book_id': args[1],
                'chapter_name': args[2],
                'chapter_id': args[3],
                'chapter_url': args[4],
                'chapter_content': args[5]
            }
        else:
            raise ReferenceError('An incorrect number of arguments is given')
        cur.execute(sql, value)
        connection.commit()

    @classmethod
    def check_book_id(cls, _id):
        """查找数据库是否存在book_id, 即查重机制
        :param _id: 传入的book_id参数"""
        sql = 'SELECT EXISTS(SELECT 1 from `笔趣阁` WHERE `id`=%(id)s)'
        value = {
            'id': _id
        }
        try:
            cur.execute(sql, value)
            return cur.fetchone()[0]
        except Exception as e:
            logger.warning('当前出现一个SQL Error: {}'.format(e))
            return 1

    @classmethod
    def check_chapter_id(cls, _id):
        """查找数据库是否存在chapter_id
        :param _id: 传入的chapter_id参数"""
        sql = 'SELECT EXISTS(SELECT 1 from `笔趣阁章节内容` WHERE `chapter_id`=%(id)s)'
        value = {
            'id': _id
        }
        try:
            cur.execute(sql, value)
            return cur.fetchone()[0]
        except Exception as e:
            logger.warning('当前出现一个SQL Error: {}'.format(e))
            return 1

