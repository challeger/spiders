# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import threading

from .utils import Proxy


class LiepinDownloaderMiddleware:
    def __init__(self):
        super().__init__()
        self.proxy_api = 'http://d.jghttp.golangapi.com/getip?num=1&type=2&pro=430000&city=430600&yys=0&port=11&pack=26095&ts=1&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='
        self.current_proxy = Proxy(self.proxy_api)
        self.lock = threading.Lock()

    def process_request(self, request, spider):
        # 更换代理
        request.meta['proxy'] = self.current_proxy.proxy_url

    def process_response(self, request, response, spider):
        if response.status != 200:
            # 如果没有正确响应,说明代理被拉黑了,设置代理状态并获取新的代理
            self.lock.acquire()
            self.current_proxy.is_blacked = True
            self.lock.release()
            # 如果请求没有被正确响应,则更换代理,并重新发送请求
            return request
        return response
