# -*- coding: utf-8 -*-
import scrapy


class SpiderGithubSpider(scrapy.Spider):
    name = 'spider_github'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/login']

    def parse(self, response):
        # 找到网页中的表单,提交数据
        yield scrapy.FormRequest.from_response(response, formdata={
            'login': '799613500@qq.com',
            'password': 'password'
        }, callback=self.after_login)

    def after_login(self, response):
        yield scrapy.Request('https://github.com/settings/profile', callback=self.visit_profile)

    def visit_profile(self, response):
        dic = response.css('#user_profile_bio::text').get()
        print(dic)
