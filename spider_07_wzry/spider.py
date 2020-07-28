#!/user/bin/env python
# 每天都要有好心情
import requests
import threading
import os
import queue
import re

from urllib import parse

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/83.0.4103.116 Safari/537.36',
    'Referer': 'https://pvp.qq.com/web201605/wallpaper.shtml'
}

URL = 'https://apps.game.qq.com/cgi-bin/ams/module/ishow/V1.0/query/workList_inc.cgi' \
      '?activityId=2735&sVerifyCode=ABCD&sDataType=JSON&iListNum=20&totalpage=0&page={}' \
      '&iOrder=0&iSortNumClose=1&_everyRead=true&iTypeId=2&iFlowId=267733&iActId=2735&iModuleId=2735'


class Module_Spider(threading.Thread):
    def __init__(self, page_queue: queue.Queue, image_queue: queue.Queue, *args, **kwargs):
        # 各页壁纸json文件路径的队列
        self.page_queue = page_queue
        # 图片队列
        self.image_queue = image_queue
        super().__init__(*args, **kwargs)
    
    @staticmethod
    def get_datas(page_url):
        resp = requests.get(page_url, headers=HEADERS)
        try:
            datas = resp.json()['List']
        except KeyError:
            return
        return datas

    @staticmethod
    def get_img_url(data):
        image_urls = []
        for i in range(1, 9):
            image_url = parse.unquote(data[f'sProdImgNo_{i}']).replace('/200', '/0')
            image_urls.append(image_url)
        return image_urls

    def run(self):
        while not self.page_queue.empty():
            datas = self.get_datas(self.page_queue.get())
            for data in datas:
                # 获取该壁纸所有尺寸的图片链接
                image_urls = self.get_img_url(data)
                # 获取该壁纸的名字,并进行一些处理
                name = re.sub('[\/:*?"<>|]', ' ', parse.unquote(data['sProdName'])).strip()
                # 设置保存路径
                dir_path = os.path.join('E:\Picture\wzry', name)

                for index, image_url in enumerate(image_urls):
                    self.image_queue.put({
                        'dir_path': dir_path,
                        'image_dir': os.path.join(dir_path, f'{index}.jpg'),
                        'image_url': image_url
                    })

        return super().run()


class Module_Save(threading.Thread):
    def __init__(self, image_queue: queue.Queue, *args, **kwargs):
        self.image_queue = image_queue
        super().__init__(*args, **kwargs)

    @staticmethod
    def save_img(image_url, image_dir):
        try:
            img = requests.get(image_url, headers=HEADERS, timeout=10)
            with open(image_dir, 'wb') as f:
                f.write(img.content)
            print(f'{image_dir}保存成功...')
        except requests.ConnectionError:
            print(f'{image_dir}保存失败...')
            return
    
    def run(self):
        while True:
            try:
                image = self.image_queue.get(timeout=10)
                # 图片的url
                image_url = image.get('image_url')
                # 图片文件夹的路径
                dir_path = image.get('dir_path')
                # 图片的保存路径
                image_dir = image.get('image_dir')
                # 判断文件夹是否存在,不存在则创建
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                
                self.save_img(image_url, image_dir)
            except (TimeoutError, queue.Empty):
                break
            except FileExistsError:
                pass

        return super().run()


def main():
    page_queue = queue.Queue(22)
    image_queue = queue.Queue(1000)
    for i in range(22):
        page_queue.put(URL.format(i))

    for _ in range(3):
        foo = Module_Spider(page_queue, image_queue, name=f'爬虫{_}号')
        foo.start()
    
    for _ in range(3):
        foo = Module_Save(image_queue, name=f'保存者{_}号')
        foo.start()


if __name__ == "__main__":
    main()
