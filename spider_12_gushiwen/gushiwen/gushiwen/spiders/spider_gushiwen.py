# -*- coding: utf-8 -*-
import re
import scrapy

from scrapy.http.response.html import HtmlResponse
from ..items import GushiwenItem


class SpiderGushiwenSpider(scrapy.Spider):
    name = 'spider_gushiwen'
    allowed_domains = ['gushiwen.org', 'gushiwen.cn']
    start_urls = ['https://www.gushiwen.cn/default_1.aspx']

    def parse(self, response: HtmlResponse):
        poems = response.css('.left > .sons')
        for poem in poems:
            # 判断一下是整首诗词还是只是句子
            title = poem.css('b::text').extract()
            item = GushiwenItem()
            if title:
                # 标题
                item['title'] = title[0]
                # [朝代,作者]
                source = poem.css('.source > a::text').extract()
                # 朝代
                item['dynasty'] = source[0]
                # 作者
                item['author'] = source[1]
                # 内容
                item['content'] = ''.join(poem.css('.contson *::text').getall()).strip()

                yield item
            else:
                # 诗句
                verses = poem.css('.cont')
                for verse in verses:
                    # 作者<<标题>>
                    source = verse.css('a::text').extract()[1]
                    # 作者
                    item['author'] = re.search(r'(.*?)《(.*?)》', source).group(1)
                    # 标题
                    item['title'] = re.search(r'(.*?)《(.*?)》', source).group(2)
                    # 句子内容
                    item['content'] = verse.css('a::text').extract()[0]
                    # 朝代
                    item['dynasty'] = ''

                    yield item

        next_href = response.css('#amore::attr(href)').get()
        if next_href:
            next_url = response.urljoin(next_href)
            request = scrapy.Request(next_url)
            yield request
