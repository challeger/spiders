# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy.http.response.html import HtmlResponse
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class JianshuDownloaderMiddleware:
    def __init__(self):
        super().__init__()

    def process_request(self, request, spider):
        print('='*30)
        print('='*30)

    def process_response(self, request, response, spider):
        print('='*30)
        return response
