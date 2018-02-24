# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BiqugeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    book_url = scrapy.Field()
    book_id = scrapy.Field()
    book_author = scrapy.Field()
    category = scrapy.Field()
    status = scrapy.Field()


class BookItem(scrapy.Item):
    num = scrapy.Field()
    chapter_name = scrapy.Field()
    chapter_url = scrapy.Field()
    chapter_id = scrapy.Field()
    book_id = scrapy.Field()
    book_name = scrapy.Field()
    chapter_content = scrapy.Field()