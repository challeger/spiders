#!/user/bin/env python
# 每天都要有好心情
import time
import requests
import redis
import urllib3

from bs4 import BeautifulSoup


class Spider:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/83.0.4103.116 Safari/537.36',
            'Referer': url
        }
        self.session = requests.Session()  # 创建一个会话
        self.session.headers = self.headers
        self.page = self.get_page_count()  # 得到总页数
        self.img_url_lists = []
        self.redis = redis.Redis(host='localhost', port=6379, db=2)
        self.key = 'mzitu'

    def get_page_count(self) -> int:
        resp = self.session.get(self.url)

        soup = BeautifulSoup(resp.text, 'lxml')
        return int(soup.find_all('a', class_='page-numbers')[-2].get_text().strip())  # 返回总页数

    def get_page_html(self, url):
        resp = self.session.get(url)
        resp.encoding = resp.apparent_encoding
        return resp

    def get_page_href(self, url):
        """
        获取页面中所有图片合集的链接
        :return:
        """
        print('正在获取页面中所有图片合集链接...')
        resp = self.get_page_html(url)

        soup = BeautifulSoup(resp.text, 'lxml')
        img_lists = soup.find('ul', attrs={'id': 'pins'}).find_all('li')
        for img_list in img_lists:
            self.img_url_lists.append(img_list.find_all('a')[1]['href'])  # 将url添加到列表中

    def get_img_page(self, url):
        """
        获取图片的所有链接
        :param url: 图片合集地址
        :return:
        """
        resp = self.get_page_html(url)
        soup = BeautifulSoup(resp.text, 'lxml')
        try:
            pages = int(soup.find('div', class_='pagenavi').find_all('a')[-2].get_text().strip())  # 获取合集中的图片数
        except AttributeError:
            print(f'获取图片总数失败..{url}')
            return
        img_base_url = self.get_img_url(url + '/1/')  # 获取图片的基础地址

        if img_base_url:
            img_url_list = [f'{img_base_url}%02d.jpg' % page for page in range(1, pages + 1)]  # 拼接图片地址,得到一个列表
            self.save_img_url(img_url_list)

    def get_img_url(self, url):
        """
        返回图片地址的截取部分,后半部分可以通过总页数来进行计算和拼接
        :param url: 图片合集地址
        :return:
        """
        resp = self.get_page_html(url)

        soup = BeautifulSoup(resp.text, 'lxml')
        try:
            img = soup.find('div', class_='main-image').find('img')['src'][:-6]
            return img
        except AttributeError:
            pass

    def save_img_url(self, url_list):
        self.redis.sadd(self.key, *url_list)

    def run(self):
        print(f'获取到总页数:{self.page}')
        for page in range(1, 5):  # 完整爬取范围应为self.page + 1
            # 将所有图片合集的链接存到一个列表中
            url = self.url + f'page/{page}/'
            print(f'正在爬取第{page}页的内容......')
            self.get_page_href(url)
            time.sleep(0.5)

        for img_url in self.img_url_lists:
            print('正在保存链接......')
            self.get_img_page(img_url)
            time.sleep(0.5)

        print(f'共保存了{len(self.img_url_lists)}个图片合集...')


if __name__ == '__main__':
    base_url = 'https://www.mzitu.com/'
    spider = Spider(base_url)
    spider.run()
