import requests
import urllib3
import time
from bs4 import BeautifulSoup
from requests import Response

"""
糗事百科/段子 https://www.qiushibaike.com/text/page/1/
同步爬虫
2020-07-02
"""


class Spider:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/83.0.4103.116 Safari/537.36'
        }
        self.page = self.get_page_count()  # 得到总页数
        self.session = requests.Session()  # 创建一个会话
    
    def get_page_count(self):
        """
        获取总页数
        :return:
        """
        resp = requests.get(self.url, headers=self.headers, verify=False)
        resp.encoding = 'UTF-8'
        soup = BeautifulSoup(resp.text, 'lxml')
        pages = soup.find('ul', class_='pagination').contents[-4].get_text().strip()

        print(f'爬取总页数: {pages}')
        return int(pages)

    def get_page_html(self, url: str):
        resp = self.session.get(url, headers=self.headers)
        resp.encoding = 'UTF-8'
        self.get_joke_data(resp)

    @staticmethod
    def get_joke_data(resp: Response):
        soup = BeautifulSoup(resp.text, 'lxml')  # 创建解析器
        jokes = soup.find_all('div', class_='article')  # 找到页面中的所有文章容器
        for joke in jokes:
            joke_author = joke.find_all('a')[1].get_text().strip()  # 作者
            joke_content = joke.find('div', class_='content').get_text().strip()  # 内容
            print(joke_author, ':', joke_content)

    def run(self):
        start = time.time()

        page_urls = [self.url + f'page/{i}/' for i in range(1, self.page + 1)]  # url列表

        for page_url in page_urls:
            self.get_page_html(page_url)  # 依次遍历页面

        print(f'总耗时:{float(time.time() - start)}')


if __name__ == "__main__":
    base_url = 'https://www.qiushibaike.com/text/'
    urllib3.disable_warnings()  # 取消移除SSL认证时的警告
    spider = Spider(base_url)
    spider.run()
