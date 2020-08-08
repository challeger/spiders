# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, HtmlResponse

from ..items import LianjiaItem


class SpiderLianjiaSpider(scrapy.Spider):
    name = 'spider_lianjia'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://www.lianjia.com/city/']

    def parse(self, response: HtmlResponse):
        """
        城市页面,解析各个城市的url,依次访问
        """
        city_urls = response.css('.city_province > ul > li > a::attr(href)').getall() 
        if city_urls:
            for url in city_urls:
                yield Request(url + 'zufang/', callback=self.parse_area)

    def parse_area(self, response: HtmlResponse):
        area_href_list = response.css('li[data-type=district] > a').getall()[1:]
        if area_href_list:
            for href in area_href_list:
                area = href.split('/')[-2]
                yield Request(f'{response.url}{area}/', callback=self.parse_page)

    def parse_page(self, response: HtmlResponse):
        page_count = response.css('div.content__pg::attr(data-totalpage)').get()
        if page_count:
            for page in (1, int(page_count) + 1):
                url = f'{response.url}pg{page}/'
                yield Request(url, callback=self.parse_housePage)
        else:
            self.parse_housePage(response)

    def parse_housePage(self, response: HtmlResponse):
        house_href_list = response.css('p.content__list--item--title > a::attr(href)').getall()
        if house_href_list:
            foo = response.url.split('/')
            base_url = f'{foo[0]}//{foo[2]}'
            for href in house_href_list:
                yield Request(base_url + href, callback=self.parse_detail)

    def parse_detail(self, response: HtmlResponse):
        item = LianjiaItem()
        # 标题
        item['title'] = response.css('p.content__title::text').get()
        # 租金
        item['rent'] = response.css('div.content__aside--title > span::text').get() +\
            response.css('div.content__aside--title::text').getall()[1].strip()
        # 租赁方式
        item['rent_way'] = response.css('ul.content__aside__list li:nth-child(1)::text').get()
        # 户型
        item['house_type'] = response.css('ul.content__aside__list li:nth-child(2)::text').get()
        # 朝向&楼层
        item['face_and_floor'] = response.css('ul.content__aside__list li:nth-child(3)::text').get()
        # 联系人
        item['contact_person'] = response.css('.contact_name::text').get()
        # 练习电话
        item['contact_tel'] = ''.join(response.css('#phone1 *::text').getall()).strip()
        # 详细信息(对字符串进行了一些处理)
        item['details'] = '\n'.join(foo.strip() for foo in response.css('div#info>ul>li::text').getall()).strip()

        yield item
