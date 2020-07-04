#!/user/bin/env python
# 每天都要有好心情
import os
import time
from multiprocessing import Process, Pipe

import urllib3

from spider_04_163.spider_163_request import Spider_163


def run(foo: Spider_163, _piep):
    foo.init()  # 初始化
    foo.login()  # 登录
    while True:
        key = _piep.recv()  # 接收主进程传入的用于搜索的关键词
        if not key:
            break
        foo.search(key)
        _piep.send(True)  # 告诉主进程爬取完成


if __name__ == '__main__':
    piep = Pipe()
    cmd = 'mitmdump -q -s spider_163_intercept.py'
    urllib3.disable_warnings()  # 取消移除SSL认证时的警告
    account = input('请输入手机号:\t')
    password = input('请输入密码:\t')

    p1 = Process(target=os.system, args=(cmd, ))

    spider = Spider_163(account, password)
    p2 = Process(target=run, args=(spider, piep[1]))
    p1.start()
    p2.start()

    # 主进程
    while True:
        keyword = input('请输入要查找的歌曲:(退出请输入Q/q)\t')
        if keyword in ('Q', 'q'):
            break
        piep[0].send(keyword)
        if piep[0].recv():  # 等待请求爬虫请求完成,再进行下一次搜索
            continue
