# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LiepinItem(scrapy.Item):
    # 职位名称
    title = scrapy.Field()
    # 职位薪资
    salary = scrapy.Field()
    # 工作城市
    city = scrapy.Field()
    # 学历要求
    edu = scrapy.Field()
    # 工作经验
    exp = scrapy.Field()
    # 年龄要求
    age = scrapy.Field()
    # 岗位描述
    desc = scrapy.Field()
