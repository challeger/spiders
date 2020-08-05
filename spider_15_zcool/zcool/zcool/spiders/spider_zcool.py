# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import ZcoolItem


class SpiderZcoolSpider(CrawlSpider):
    name = 'spider_zcool'
    allowed_domains = ['zcool.com.cn']
    start_urls = ['https://www.zcool.com.cn/discover/1!0!0!0!0!!!!2!-1!1']

    rules = (
        # 翻页的url
        Rule(LinkExtractor(allow=r'/discover/1!0!0!0!0!!!!2!-1!\d+'), follow=True),
        # 图片合集的url
        Rule(LinkExtractor(allow=r'.+/work/.+\.html'), callback='parse_detail', follow=False)
    )

    def parse_detail(self, response):
        item = ZcoolItem()
        # 图片合集的标题 对win10中文件夹不允许的字符进行了替换
        item['img_title'] = re.sub(r'[\\/:*?"<>|]', '',
                                   response.css('h2::text').get().strip())
        # 图片作者 对win10中文件夹不允许的字符进行了替换
        item['img_author'] = re.sub(r'[\\/:*?"<>|]', '',
                                    response.css('.author-info-title > a *::text').get().strip())
        # 图片合集中各图片的url
        item['image_urls'] = response.css('.photo-information-content > img::attr(src)').getall()

        yield item
