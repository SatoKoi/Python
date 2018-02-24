# -*- coding:utf-8 -*-
__author__ = 'KoiSato'

from ..items import BiqugeItem, BookItem
from .sql import Sql
from scrapy.log import logger


class BiqugePipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, BiqugeItem):
            flag = 1
            name = item['name']
            author = item['book_author']
            _id = item['book_id']
            url = item['book_url']
            category = item['category']
            status = item['status']
            ret = Sql.check_book_id(_id)
            if ret != 1:
                Sql.insert_message(name, author, category, status, url, _id, flag=flag)
            else:
                logger.info('该书 {} 已存在数据库'.format(name))

        if isinstance(item, BookItem):
            flag = 2
            num = item['num']
            chapter_name = item['chapter_name']
            chapter_url = item['chapter_url']
            chapter_id = item['chapter_id']
            book_id = item['book_id']
            book_name = item['book_name']
            chapter_content = item['chapter_content']
            ret = Sql.check_chapter_id(chapter_id)
            if ret != 1:
                Sql.insert_message(book_name, book_id, chapter_name, chapter_id, chapter_url, chapter_content, flag=flag)
            else:
                logger.info('该章节 {} {} 已存在数据库'.format(book_name, chapter_name))
        return item
