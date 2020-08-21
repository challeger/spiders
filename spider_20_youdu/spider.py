"""
需要的功能:
    登录
    获取书架上的书籍
    获取书籍中的文章
    订阅章节
    获取对应章节的信息(包括查看书评)
    充值
"""
import requests
import re
import base64
import urllib3
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
    'cookie': '登录的cookie',
    'origin': 'https://www.youdubook.com',
    'x-requested-with': 'XMLHttpRequest'
}


class Spider_Youdu:
    def __init__(self):
        super().__init__()
        self.session = requests.session()
        # 设置cookies直接模拟登录
        self.session.headers = HEADERS
        # 取消SSL认证
        self.session.verify = False
        self.my_books = {}
        self.my_wallet = {}

    def get_user_center(self):
        # 书架信息
        books_url = 'https://www.youdubook.com/user/favobook'
        # 钱包信息
        money_url = 'https://www.youdubook.com/user/prepaidrecords'

        # 获取书架信息
        resp = self.session.get(books_url)
        soup = BeautifulSoup(resp.text, 'lxml')
        watching_books = soup.find('div', class_='favoList').findAll('li')

        # 获取钱包信息
        resp = self.session.get(money_url)
        soup = BeautifulSoup(resp.text, 'lxml')
        my_wallet = soup.find('div', class_='Top').findAll('li')
        for book in watching_books:
            book_title = book.find('a')['title']
            new_chapter = book.find('div', class_='updateChapter').find('a')
            self.my_books[book_title] = {
                '书名': book_title,
                '书籍链接': book.find('a')['href'],
                '最新章节名': new_chapter.get_text().strip(),
                '最新章节链接': new_chapter['href']
            }
        self.my_wallet['推荐票'] = my_wallet[0].find('em').get_text()
        self.my_wallet['月票'] = my_wallet[1].find('em').get_text()
        self.my_wallet['SAN值'] = my_wallet[2].find('em').get_text()
        self.my_wallet['临时SAN值'] = my_wallet[3].find('em').get_text()

    def get_chapter_json(self, chapter_id):
        """
        获取指定id章节的数据
        """
        # 需要从网页源码中的javascript代码中获取到需要的表单数据
        html_url = f'https://www.youdubook.com/readchapter/{chapter_id}'
        # 获得章节json数据的url
        json_url = f'https://www.youdubook.com/booklibrary/membersinglechapter/chapter_id/{chapter_id}'
        resp = self.session.get(html_url)
        # 通过正则获取到需要的数据
        caonima = re.findall(r'MemberSingleChapter.+?;', resp.text)[-1].split('"')[-2]
        data = {
            'sign': 'a3NvcnQoJHBhcmEpOw==',
            'caonima': caonima
        }
        # 获取章节数据需要的headers
        self.session.headers.update({
            'referer': html_url
        })
        # 响应
        resp = self.session.post(json_url, data=data)
        return resp.json()['data']

    def get_line_json(self, chapter_id, count, index):
        line_url = 'https://www.youdubook.com/booklibrary/tsukkomilist'
        data = {
            'page': 1,
            'count': count,
            'chapter_id': chapter_id,
            'paragraph_index': index
        }
        resp = self.session.post(line_url, data=data)
        return resp.json()['data']['data']

    def get_book_detail(self, book_url):
        resp = self.session.get(book_url)
        soup = BeautifulSoup(resp.text, 'lxml')
        # 书籍标题+作者
        book_title = soup.find('div', class_='title')
        # 书籍简介
        book_disc = soup.find('div', class_='synopsisCon')
        # 书籍卷名
        book_volume_list = soup.findAll('div', class_='volume_name')
        # 书籍章节列表
        book_chapter_list = soup.findAll('div', class_='chapter_list')
        print(book_title)
        print(book_disc)
        print(book_volume_list)
        print(book_chapter_list)

    def buy_chapter(self, book_id, chapter_id):
        # 订阅指定章节
        buy_url = 'https://www.youdubook.com/booklibrary/subscribebookaction'
        data = {
            'BookID': book_id,
            'ChapterID': chapter_id,
            'isSingleWsCount': 0,
            'isAllWsCount': 0,
            'isMethod': 1,
            'isAuto': 0
        }
        resp = self.session.post(buy_url, data=data)
        print(f'章节{chapter_id}|{resp.json()["msg"]}')

    @staticmethod
    def parse_chapter_content(json_data):
        # 将拿到的章节信息进行解析
        content = []
        print(json_data['title'])
        for line in json_data['show_content']:
            # 章节内容进行了base64加密,所以进行base64解密
            content.append({
                'index': line['paragraph_index'],
                'content': base64.b64decode(line['content']).decode('utf-8').strip(),
                'tsukkomi': line['tsukkomi']
            })
        print(content)

    @staticmethod
    def parse_line_content(json_data):
        for data in json_data:
            user_id = data['theUser']
            user_name = data['nickname']
            content = data['tsukkomi_content']
            add_time = data['addTime']
            print(f'[{add_time}]{user_name}:{content}')

    def run(self):
        # data = self.get_chapter_json(126427)
        # self.parse_chapter_content(data)
        # self.get_book_detail('https://www.youdubook.com/book_detail/1917')
        data = self.get_line_json(126427, 6, 45)
        self.parse_line_content(data)


if __name__ == "__main__":
    urllib3.disable_warnings()
    s1 = Spider_Youdu()
    s1.run()
