# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import LieyunItem


class SpiderLieyunSpider(CrawlSpider):
    name = 'spider_lieyun'
    allowed_domains = ['lieyunwang.com']
    start_urls = ['https://www.lieyunwang.com/']

    rules = (
        Rule(LinkExtractor(allow=r'/latest/p\d+\.html'), follow=True),
        Rule(LinkExtractor(allow=r'/archives/\d+'), callback='parse_detail', follow=False),
    )

    def parse_detail(self, response):
        item = LieyunItem()

        # 文章标题
        item['title'] = response.css('.lyw-article-title-inner *::text').getall()[-1].strip()
        # 文章发布时间
        item['pub_time'] = response.css('.lyw-article-title-inner *::text').getall()[1]
        # 文章作者
        item['author'] = response.css('.author-name::text').get()
        # 文章内容
        item['content'] = response.css('.main-text').get()
        # 原文链接
        item['origin'] = response.url

        return item
