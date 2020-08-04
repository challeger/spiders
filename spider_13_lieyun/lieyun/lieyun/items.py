# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LieyunItem(scrapy.Item):
    # 标题
    title = scrapy.Field()
    # 发布时间
    pub_time = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 内容
    content = scrapy.Field()
    # 原链接
    origin = scrapy.Field()
