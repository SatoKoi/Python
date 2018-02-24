# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup as bs
import re
from ..items import BiqugeItem, BookItem


class MainSpider(scrapy.Spider):
    name = 'main'
    allowed_domains = ['www.biquge5200.com']
    start_urls = ['http://www.biquge5200.com/xiaoshuodaquan/']

    def parse(self, response):
        """解析初始页, 产生后续url, 爬取需要存储的信息，整个流程是异步、递归实现的"""
        soup = bs(response.text, 'html.parser')
        novel_lists = soup.find_all('div', class_='novellist')
        for novel_list in novel_lists:
            list_novels = novel_list.find_all('a')
            for list_novel in list_novels:
                start_url = list_novel['href']
                sibling_node = True if list_novel.next_sibling else False
                if sibling_node:
                    status = '完本'
                else:
                    status = '连载'
                res = re.search(r'_(\d+)/', start_url)
                book_id = res.group(1) if res else 'undefined'
                name = list_novel.get_text()
                # 生成新的URL并跟进
                yield scrapy.Request(start_url, callback=self.get_other, meta={'book_url': start_url,
                                                                               'book_id': book_id,
                                                                               'name': name,
                                                                               'status': status})

    def get_other(self, response):
        """获取该书的其他信息"""
        item = BiqugeItem()
        soup = bs(response.text, 'html.parser')
        alink = soup.find('div', class_='con_top').find_all('a')[2]
        category = alink.get_text()
        info_text = soup.find('div', id='maininfo').find('div', id='info').find('p').get_text()
        res = re.search(r'：(\w+)', info_text)
        item['book_author'] = res.group(1) if res else 'N/A'
        item['name'] = response.meta['name']
        item['book_id'] = response.meta['book_id']
        item['book_url'] = response.meta['book_url']
        item['status'] = response.meta['status']
        item['category'] = category
        yield item

        num = 0
        all_chapter_links = soup.find_all('dd')[9:-1]
        for link in all_chapter_links:
            chapter_id = re.search(r'/(\d+)\.html', str(link)).group(1)
            a_link = link.find('a')
            chapter_name = a_link.get_text()
            chapter_url = a_link['href']
            num += 1
            yield scrapy.Request(chapter_url, callback=self.get_chapter_content, meta={'chapter_url': chapter_url,
                                                                                       'chapter_id': chapter_id,
                                                                                       'num': num,
                                                                                       'chapter_name': chapter_name,
                                                                                       'book_id': response.meta['book_id'],
                                                                                       'book_name': response.meta['name']})

    def get_chapter_content(self, response):
        """获取该书的章节信息"""
        item = BookItem()
        item['chapter_url'] = response.meta['chapter_url']
        item['chapter_id'] = response.meta['chapter_id']
        item['num'] = response.meta['num']
        item['book_id'] = response.meta['book_id']
        item['book_name'] = response.meta['book_name']
        item['chapter_name'] = response.meta['chapter_name']
        soup = bs(response.text, 'html.parser')
        content = soup.find('div', id='content').get_text()
        item['chapter_content'] = self.strip(content)
        return item

    def strip(self, string):
        """删除多余的符号"""
        string = re.sub(r'["|\'\s]', '', string)
        return re.sub(r'<br>|</br>', '\n', string)

