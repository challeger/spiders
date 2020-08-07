# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import LiepinItem


class SpiderLiepinSpider(CrawlSpider):
    name = 'spider_liepin'
    allowed_domains = ['liepin.com']
    start_urls = ['https://www.liepin.com/zhaopin/?key=python']

    rules = (
        # 翻页url规则
        Rule(LinkExtractor(allow=r'/zhaopin/.+?curPage=\d+', restrict_css='.pagerbar'), follow=True),
        # 职位url规则
        Rule(LinkExtractor(allow=r'https://www.liepin.com/job/\d+\.shtml', restrict_css='.job-info'),
             callback='parse_item'),
    )

    def parse_item(self, response):
        item = LiepinItem()

        item['title'] = response.css('.title-info h1::text').get()
        item['salary'] = response.css('.job-item-title::text').get().strip()
        item['city'] = response.css('.basic-infor span a::text').get()
        item['edu'] = response.css('.job-qualifications span:nth-child(1)::text').get()
        item['exp'] = response.css('.job-qualifications span:nth-child(2)::text').get()
        item['age'] = response.css('.job-qualifications span:nth-child(4)::text').get()
        item['desc'] = ''.join(response.css('.job-description > .content *::text').getall()).strip()

        return item
