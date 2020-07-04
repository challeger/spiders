#!/user/bin/env python
# 每天都要有好心情
import os
import re
import json
import mitmproxy
import requests
from concurrent.futures import ThreadPoolExecutor

"""
监听指定接口,抓取其返回的json数据,从json数据中获取歌曲id与歌曲文件url
通过url抓取m4a文件并保存到本地
"""

pool = ThreadPoolExecutor(max_workers=4)


def save_music(s_id, s_url):
    song_url = f'https://music.163.com/song?id={s_id}'  # 歌曲详情页面
    save_url = 'E:/Music/'  # 歌曲保存路径

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/83.0.4103.116 Safari/537.36',
        'Referer': 'https://music.163.com/'
    }
    resp = requests.get(song_url, headers=headers, verify=False)  # 获取歌曲信息
    resp.encoding = resp.apparent_encoding
    title = re.search('<title>(.*?)</title>', resp.text).group(1)  # 歌曲名
    title = re.sub(r'[/\?*":<>|]', '', title)  # 文件名过滤,防止有不符合规则的命名

    save_path = f'{save_url}{title}.m4a'
    if os.path.exists(save_path):
        print(f'{save_url}{title}.m4a已保存,跳过')
        return

    resp = requests.get(s_url, headers=headers)  # 获取歌曲文件
    print(f'正在保存{title}.m4a')
    with open(save_path, 'ab') as song:  # 保存
        song.write(resp.content)
        song.flush()


def response(flow):
    global pool
    url = 'https://music.163.com/weapi/song/enhance/player/url/'
    if url in flow.request.url:
        text = json.loads(flow.response.text)['data'][0]
        try:
            song_id = text['id']
            song_url = text['url']
            print(f'获取到url:{song_url},正在保存...')
            pool.submit(save_music, song_id, song_url)
        except KeyError:
            print('未获取到url')
