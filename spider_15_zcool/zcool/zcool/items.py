# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZcoolItem(scrapy.Item):
    # 图片合集标题
    img_title = scrapy.Field()
    # 图片合集作者
    img_author = scrapy.Field()
    # 图片合集链接
    image_urls = scrapy.Field()
    # 图片对象
    images = scrapy.Field()
