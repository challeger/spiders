import requests
import time
import random
import hashlib


class Spider_Translate:
    BASE_URL = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    HEADERS = {
        'Host': 'fanyi.youdao.com',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        'Referer': 'http://fanyi.youdao.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': '_ntes_nnid=ef63d6c3863fb70b16ea34fafa9c4c22,1589272466388; OUTFOX_SEARCH_USER_ID_NCOO=1901841316.1985073; OUTFOX_SEARCH_USER_ID=-890377116@175.5.179.41; UM_distinctid=172ee321051134-074ffd1d17dc42-4353760-232800-172ee32105266b; JSESSIONID=aaaeqg5z_FPR6az6DFJox; ___rl__test__cookies=1596176277803',
    }

    @staticmethod
    def encrypt(keyword):
        salt = str(time.time() * 1000) + str(random.randint(0, 10))
        temp = 'fanyideskweb' + keyword + salt + 'mmbP%A-r6U3Nw(n]BjuEU'
        sign = hashlib.md5(temp.encode('utf-8')).hexdigest()

        return {
            'i': keyword,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': salt,
            'sign': sign,
            'bv': '7b07590bbf1761eedb1ff6dbfac3c1f0',
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_REALTlME',
        }

    def translate(self, keyword):
        data = self.encrypt(keyword)
        try:
            resp = requests.post(Spider_Translate.BASE_URL, headers=Spider_Translate.HEADERS, data=data).json()['translateResult']
            print(f'翻译结果:{resp[0][0]["tgt"]}')
        except KeyError as e:
            print(e)


if __name__ == "__main__":
    foo = Spider_Translate()
    while True:
        foo.translate(input('请输入要翻译的关键词:\t'))
