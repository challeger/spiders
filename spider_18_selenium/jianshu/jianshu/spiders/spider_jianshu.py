# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http.response.html import HtmlResponse
from scrapy_selenium import SeleniumRequest


class SpiderJianshuSpider(CrawlSpider):
    name = 'spider_jianshu'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/p/be81b1987af1']

    rules = (
        Rule(LinkExtractor(allow=r'/p/[0-9a-z]{12}'), callback='parse_item', follow=True),
    )

    def parse_item(self, response: HtmlResponse):
        # categroy = response.css('div#note-page-comment+section>div>a>span::text').getall()
        print('='*30)
        print(response.css('div[role=main] section')[0].css('h1::text').get())
        print('='*30)

    def _build_request(self, rule_index, link):
        return SeleniumRequest(
            url=link.url,
            callback=self._callback,
            errback=self._errback,
            meta=dict(rule=rule_index, link_text=link.text),
        )
