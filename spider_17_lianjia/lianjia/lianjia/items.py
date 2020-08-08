# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # 标题
    title = scrapy.Field()
    # 租金
    rent = scrapy.Field()
    # 租赁方式
    rent_way = scrapy.Field()
    # 户型
    house_type = scrapy.Field()
    # 朝向&楼层
    face_and_floor = scrapy.Field()
    # 联系人
    contact_person = scrapy.Field()
    # 联系电话
    contact_tel = scrapy.Field()
    # 详细信息
    details = scrapy.Field()
