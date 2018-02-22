# coding=utf-8

from scrapy import Request
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from .. import items


class Spider(CrawlSpider):
    """爬虫类, 继承自scrapy.spider.CrawlSpider
    param name: 爬虫名称
    param start_urls: 初始爬取的URL
    param img_urls: 爬取到的图片URL放在该list里
    param rule: 爬取规则, 为一个元组, 存放Rule类进行规则管理
    param allowed_domains: 可供爬取的域名
    param Rule: attr1: LinkExtractor: 定义如何从爬取到的页面提取链接
                attr2: callback: 回调函数, Spider中同名函数将被调用, 其接受response作为第一个参数
                attr3: follow: 布尔值, 表示是否跟进从response中提取的链接
    param LinkExtractor: attr1: allow: 允许访问的网址名, 可接受正则表达式
                         attr2: deny: 禁止访问的网址名, 可接受正则表达式
    """
    name = 'mzitu'
    start_urls = ['http://www.mzitu.com/']
    img_urls = []
    allowed_domains = ['mzitu.com']
    rules = (
        Rule(LinkExtractor(allow=('http://www.mzitu.com/\d{1,6}',),
                           deny=('http://www.mzitu.com/\d{1,6}/\d{1,6}',)),
             callback='parse_item',
             follow=True),
    )

    def parse_item(self, response):
        """
        :param response: 下载器返回的response
        param item: 存储模板实例
        param max_num: 该页最大页数
        func extract_first() 获取extract()结果list中的第一个数据
        """
        item = items.MzituScrapyItem()
        # max_num为页面最后一张图片的位置
        max_num = response.xpath("descendant::div[@class='main']/div[@class='content']/div[@class='pagenavi']/a[last()-1]/span/text()").extract_first(default="N/A")
        item['name'] = response.xpath("./*//div[@class='main']/div[1]/h2/text()").extract_first(default="N/A")
        item['url'] = response.url
        for num in range(1, int(max_num)):
            # page_url 为每张图片所在的页面地址
            page_url = response.url + '/' + str(num)
            yield Request(page_url, callback=self.img_url)
        # 获取该套图的所有图片地址
        item['image_urls'] = self.img_urls
        yield item

    def img_url(self, response):
        """取出图片URL 并添加进self.img_urls列表中
        :param response:
        param img_url 为每张图片的真实地址
        """
        img_urls = response.xpath("descendant::div[@class='main-image']/descendant::img/@src").extract()
        for img_url in img_urls:
            self.img_urls.append(img_url)
