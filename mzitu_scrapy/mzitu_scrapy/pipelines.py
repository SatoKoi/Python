# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import re


class MzituScrapyPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        """
        :param request: 每一个图片下载管道请求
        :param response: None
        :param info: None
        param strip :清洗Windows系统的文件夹非法字符，避免无法创建目录
        :return: 每套图的分类目录
        """
        item = request.meta['item']
        category = item['category']
        folder = item['name']
        folder_strip = strip(folder)
        image_guid = request.url.split('/')[-1]
        filename = u'{2}/{0}/{1}'.format(folder_strip, image_guid, category)
        return filename

    def get_media_requests(self, item, info):
        """
        :param item: spider.py中返回的item
        :param info:
        :return:
        """
        for img_url in item['image_urls']:
            referer = item['url']
            yield Request(img_url, meta={'item': item,
                                         'referer': referer})

    def item_completed(self, results, item, info):
        """当一个单独项目的所有图片完成请求时, 该方法被调用,
        此方法决定是否返回或丢弃项目
        :param results: 二元组: attr1: success, attr2: image_info_or_error
        attr: success: 布尔值, 成功下载时为True
        attr: image_info_or_error: success为True时, 返回一个包含下列关键字的字典:
              url: 图片下载的url, path: 图片存储的路径, checksum: 图片内容的MD5hash;
              success为False时, 返回一个Twisted Failure信息
        :param item: 存储模板
        :return: 返回项目"""
        image_paths = [x['path'] for ok, x in results if ok]
        # 丢弃项目
        if not image_paths:
            raise DropItem("Item contains no images")
        return item

        # def process_item(self, item, spider):
        #     return item


def strip(path):
    """
    :param path: 需要清洗的文件夹名字
    :return: 清洗掉Windows系统非法文件夹名字的字符串
    """
    path = re.sub(r'[？\\*|“<>:/]', '', str(path))
    return path

