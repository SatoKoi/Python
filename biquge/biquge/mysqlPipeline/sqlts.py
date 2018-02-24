# -*- coding:utf-8 -*-
# from .sql import Sql
import pymysql
from biquge.biquge import settings

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
sql = 'SELECT EXISTS(SELECT 1 FROM `笔趣阁` where id="132222")'
cur.execute(sql)
print(cur.fetchone()[0])
