#!/user/bin/env python
# 每天都要有好心情
import time
import re
import datetime

import requests
from bs4 import BeautifulSoup

from spider_proxies import get_proxies


class Spider:
    def __init__(self):
        self.session = requests.session()  # 创建一个会话
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/83.0.4103.116 Safari/537.36'
        }

    def crawl_all_av(self, mid):
        """
        输入用户的UID,爬取用户的所有视频信息
        :param mid: 用户uid
        :return:
        """
        base_url = 'https://api.bilibili.com/x/space/arc/search?mid={}&ps=30&pn={}&jsonp=jsonp'
        pn = 1  # 从第一页开始
        while True:
            if pn % 5 == 1:
                self.session.proxies = get_proxies()  # 爬取5页换一个代理ip
            url = base_url.format(mid, pn)
            video_list = self.session.get(url).json()['data']['list']['vlist']
            if video_list:
                for video in video_list:
                    video_aid = video['aid'].strip()  # aid
                    video_bv = video['bvid'].strip()  # bv号
                    video_title = video['title']  # 标题
                    video_desc = video['description']  # 简介
                    video_play = video['play']  # 播放量
                    video_comment = video['comment']  # 评论量
                    video_pic = 'http:' + video['pic']  # 视频封面链接
                    print(f'{video_title} || {video_bv} || {video_play} || {video_comment}')
            else:
                # 没有数据说明已经全部爬完了
                break
            time.sleep(1)

    def crawl_video_barrage(self, cid):
        """
        根据视频的cid,获取1000条弹幕
        :param cid: 视频的cid
        :return:
        """
        url = f'https://api.bilibili.com/x/v1/dm/list.so?oid={cid}'
        resp = self.session.get(url)
        resp.encoding = resp.apparent_encoding  # 编码
        soup = BeautifulSoup(resp.text, 'lxml')
        barrage_lists = soup.find_all('d')
        for barrage in barrage_lists:
            barrage_content = barrage.get_text()  # 弹幕内容

            barrage_info = barrage['p'].split(',')
            barrage_sender = int(barrage_info[6].strip(), 16)  # 转为10进制,发送者的uid
            barrage_send_time = datetime.datetime.fromtimestamp(int(barrage_info[4].strip()))  # 发送时间
            print(f'[{barrage_send_time}]{barrage_sender}: {barrage_content}')

    def crawl_search_user(self, keyword):
        """
        根据关键词搜索用户,返回搜索列表的前五个用户的信息
        :param keyword: 搜索关键字
        :return:
        """
        search_url = f'https://search.bilibili.com/upuser?keyword={keyword}'
        resp = self.session.get(search_url)
        resp.encoding = resp.apparent_encoding

        soup = BeautifulSoup(resp.text, 'lxml')
        users_list = soup.find_all('li', class_='user-item')
        for user in users_list[:5]:
            try:
                user_name = user.find('a', class_='title').get_text().strip()  # 用户昵称
                foo = user.find('a', class_='title')['href']
                user_id = re.search(r'/(\d+)', foo).group(1)  # 用户Uid
                user_fans = user.find('div', class_='up-info clearfix').find_all('span')[1].get_text()  # 用户粉丝
                user_desc = user.find('div', class_='desc').get_text().strip()  # 用户简介
                print(f'uid:[{user_id}] 用户名:{user_name} {user_fans} 用户简介:{user_desc}')

            except AttributeError:
                print('未查找到指定元素')
                continue

    def crawl_search_video(self, keyword):
        """
        根据关键词搜索视频,返回搜索结果的前十个视频的信息
        :param keyword: 搜索的关键词
        :return:
        """
        search_url = f'https://search.bilibili.com/video?keyword={keyword}'
        resp = self.session.get(search_url)
        resp.encoding = resp.apparent_encoding

        soup = BeautifulSoup(resp.text, 'lxml')
        video_list = soup.find_all('li', class_='video-item matrix')  # 视频列表

        for video in video_list[:10]:
            try:
                video_title = video.find('a', class_='title').get_text().strip()  # 视频标题
                video_link = 'https:' + video.find('a', class_='title')['href']  # 视频链接
                video_up = video.find('a', class_='up-name').get_text().strip()  # 视频up昵称
                video_play = video.find('span', class_='so-icon watch-num').get_text().strip()  # 视频播放量
                video_comment = video.find('span', attrs={'title': '弹幕'}).get_text().strip()  # 视频弹幕量
                video_create_time = video.find('span', class_='so-icon time').get_text().strip()  # 视频发布时间
                print(f'{video_title}[{video_up}] 播放:{video_play} 弹幕:{video_comment} 发布时间:{video_create_time}\n'
                      f'链接:{video_link}')
            except (AttributeError, IndexError):
                print('未检索到指定内容')
                continue


if __name__ == '__main__':
    spider = Spider()
    # spider.crawl_all_av('777536')
    # spider.crawl_video_barrage('207327869')
    spider.crawl_search_video('lex')
