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
import threading
import re
import base64
import urllib3
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
    'cookie': 'saveMemberInfo=%7B%22username%22%3A%2218890035791%22%2C%22password%22%3A%22T85568397%22%7D;',
    'origin': 'https://www.youdubook.com',
    'x-requested-with': 'XMLHttpRequest'
}


class Spider_Youdu:
    _instance_lock = threading.Lock()

    def __init__(self):
        super().__init__()
        self.session = requests.session()
        # 设置cookies直接模拟登录
        self.session.headers = HEADERS
        # 取消SSL认证
        self.session.verify = False
        self.my_books = {}
        self.my_wallet = {}

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = object.__new__(cls)  
        return cls._instance

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
        print(watching_books)
        for book in watching_books:
            book_title = book.find('a')['title']
            new_chapter = book.find('div', class_='updateChapter').find('a')
            self.my_books[book_title] = {
                '书名': book_title,
                '书籍链接': book.find('a')['href'].split('/')[-1],
                'book_pic': book.find('img')['data-original'],
                '最新章节名': new_chapter.get_text().strip(),
                '最新章节链接': new_chapter['href']
            }
        print(self.my_books)
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
        title_author = soup.find('div', class_='title')
        book_data = {
            'book_title': title_author.find('span').get_text().strip(),
            'book_author': title_author.find('em').get_text().strip(),
            'book_disc': soup.find('div', class_='synopsisCon').get_text().strip(),
            'book_volume_list': []
        }
        # 书籍卷名
        book_volume_list = soup.findAll('div', class_='volume_name')
        book_chapter_list = soup.findAll('div', class_='chapter_list')
        for volume in book_volume_list:
            book_data['book_volume_list'].append({
                'volume_name': volume.get_text().strip(),
                'chapter_list': []
            })
        for volume in book_data['book_volume_list']:
            for book_chapter in book_chapter_list:
                chapter_list = book_chapter.findAll('a')
                for chapter in chapter_list:
                    volume['chapter_list'].append({
                        'chapter_title': chapter.get_text().strip(),
                        'chapter_href': chapter['href']
                    })
        print(book_data)

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
        print(resp.json())

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

    def get_rank_html(self, rank_type='Favo', page=1, data_type='Week'):
        base_url = f'https://www.youdubook.com/ranking/ranklist/tag/{rank_type}/type/{data_type}?page={page}'
        resp = self.session.get(base_url)
        soup = BeautifulSoup(resp.text, 'lxml')
        book_list = soup.find('div', class_='piclist').findAll('li')
        for book in book_list:
            # id
            book_id = book.find('a')['href'].split('/')[-1]
            # 标题
            book_title = book.find('a')['title']
            # 封面
            book_cover = book.find('img')['data-original']
            # 作者
            book_author = book.find('div', class_='nicheng').get_text().strip()
            # 收藏
            book_favo = book.find('div', class_='shoucang').get_text().strip()
            # 人气
            book_popalrity = book.find('div', class_='renqi').get_text().strip()
            print('='*30)
            print(f'{book_id}:{book_title}-{book_author}|{book_cover}|{book_favo}{book_popalrity}')

    def search(self, keyword, page=None):
        url = f'https://www.youdubook.com/booklibrary/index/str/0_0_0_0_0_0_0_{keyword}?page={page}'
        resp = self.session.get(url)
        soup = BeautifulSoup(resp.text, 'lxml')
        book_list = soup.find('div', class_='BooklibraryList').findAll('li', class_='')[:-1]
        book_page = soup.find('div', class_='pageInfo').findAll('em')
        pages = book_page[-3].get_text() if book_page else 0
        print(pages)
        for book in book_list:
            # id
            book_id = book.find('a')['href'].split('/')[-1]
            # 标题
            book_title = book.find('a')['title']
            # 封面
            book_cover = book.find('img', class_='img1')['data-original']
            # 作者
            book_author = book.find('dd', class_='nickname').get_text().strip()
            # 收藏
            book_favo = book.find('dd', class_='favo').get_text().strip()
            # 人气
            book_popalrity = book.find('dd', class_='hit').get_text().strip()
            print('='*30)
            print(f'{book_id}:{book_title}-{book_author}|{book_cover}|{book_favo}{book_popalrity}')

    def favo_book(self, book_id):
        url = 'https://www.youdubook.com/booklibrary/actionfavo'
        data = {
            'BookID': book_id
        }
        resp = self.session.post(url, data)
        print(resp.json())

    def run(self):
        # self.get_user_center()
        # data = self.get_chapter_json(126427)
        # print(data)
        # self.parse_chapter_content(data)
        # self.get_book_detail('https://www.youdubook.com/book_detail/1917')
        # data = self.get_line_json(126427, 6, 45)
        # self.parse_line_content(data)
        # self.get_rank_html(rank_type='Hit', data_type='Month', page=2)
        # self.search('弗雷尔卓德的孤狼')
        self.favo_book(587)


if __name__ == "__main__":
    urllib3.disable_warnings()
    s1 = Spider_Youdu()
    s1.run()
