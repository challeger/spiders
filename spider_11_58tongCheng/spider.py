import io
import re
import base64
import requests

from fontTools.ttLib import TTFont
from bs4 import BeautifulSoup


class Module_Spider:
    def __init__(self):
        self.baseUrl = 'https://yongzhou.58.com/chuzu/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        }
        # 字体文件
        self.currentFont = self.get_font()
        # 字体名与文字映射
        self.number_to_shape = self.set_number_to_shape()
        # 十六进制编号与文字映射
        self.code_to_number = self.set_code_to_number()

    def get_font(self):
        """
        从网页源代码中获取base64编码,并转换为ttfont类
        """
        resp = requests.get(self.baseUrl, headers=self.headers)
        font_face = re.search(r"@font-face.+?base64,(.+?)'\)", resp.text).group(1)
        return TTFont(io.BytesIO(base64.b64decode(font_face)))

    def set_number_to_shape(self):
        """
        根据ttfont类中的glyf,建立number->shape的映射关系
        """
        font_glyf = self.currentFont['glyf']

        return {
            0: font_glyf['glyph00001'],
            1: font_glyf['glyph00002'],
            2: font_glyf['glyph00003'],
            3: font_glyf['glyph00004'],
            4: font_glyf['glyph00005'],
            5: font_glyf['glyph00006'],
            6: font_glyf['glyph00007'],
            7: font_glyf['glyph00008'],
            8: font_glyf['glyph00009'],
            9: font_glyf['glyph00010'],
        }

    def set_code_to_number(self):
        """
        建立code->文字的映射
        """
        # 获取xml中的cmap部分,也就是code与name的映射
        codeNameMap = self.currentFont.getBestCmap()
        # xml的glyf部分,name与sharp的映射
        font_glyf = self.currentFont['glyf']

        foo_map = {}
        for code, name in codeNameMap.items():
            font_shape = font_glyf[name]
            code = str(hex(code)).replace('0', '&#', 1) + ';'
            number = [number for number, shape in self.number_to_shape.items() if shape == font_shape][0]
            foo_map[code] = number

        return foo_map

    def get_html_text(self, url):
        """
        请求目标网址,并将获得的网页源码中的字体code替换为对应number
        """
        try:
            html = requests.get(url, self.headers).text
            for code, number in self.code_to_number.items():
                html = re.sub(f'{code}', str(number), html)
            return html
        except Exception as e:
            print(e)

    def parse(self, html):
        """
        解析网页源代码,获得需要的信息
        """
        soup = BeautifulSoup(html, 'lxml')
        house_list = soup.findAll(class_='house-cell')
        for house in house_list:
            try:
                house_title = house.find('a', class_='strongbox').get_text().strip()
                house_config = house.find('p', class_='room').get_text().strip()
                house_price = house.find('div', class_='money').get_text().strip()
                print(f'{house_title} -- {house_config} -- {house_price}')
            except AttributeError as e:
                print(e)

    def run(self):
        url = self.baseUrl + 'pn{}/'
        for i in range(1, 71):
            self.parse(self.get_html_text(url.format(i)))


if __name__ == "__main__":
    spider = Module_Spider()
    spider.run()
