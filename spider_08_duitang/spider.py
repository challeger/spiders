#!/user/bin/env python
# 每天都要有好心情
import os

import requests
import threading
import queue


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/83.0.4103.116 Safari/537.36'
}

URL = 'https://www.duitang.com/napi/blog/list/by_filter_id/?filter_id=%E5%A4%B4%E5%83%8F&start={}'
SAVE_DIR = 'E:\Picture\head'


class Module_Spider(threading.Thread):
    def __init__(self, page_queue: queue.Queue, image_queue: queue.Queue, *args, **kwargs):
        # 各页头像json文件路径的队列
        self.page_queue = page_queue
        # 图片链接队列
        self.image_queue = image_queue
        super(Module_Spider, self).__init__(*args, **kwargs)

    @staticmethod
    def get_data(url):
        """
        获取url中的json数据,并返回
        :param url: 图片列表url
        :return:
        """
        resp = requests.get(url, headers=HEADERS)
        try:
            data = resp.json()['data']['object_list']
        except KeyError:
            return None
        return data

    def run(self) -> None:
        while not self.page_queue.empty():
            # 获取图片列表
            photo_list = self.get_data(self.page_queue.get())
            for photo in photo_list:
                try:
                    self.image_queue.put(photo['photo']['path'])
                except KeyError:
                    continue

        return super(Module_Spider, self).run()


class Module_Save(threading.Thread):
    def __init__(self, image_queue: queue.Queue, *args, **kwargs):
        self.image_queue = image_queue
        super(Module_Save, self).__init__(*args, **kwargs)

    @staticmethod
    def save_img(image_url, save_dir):
        try:
            img = requests.get(image_url, timeout=10)
            with open(save_dir, 'wb') as f:
                f.write(img.content)
            print(f'{image_url}保存成功..')
        except (requests.ConnectionError, OSError):
            print(f'{image_url}保存失败..')

    def run(self) -> None:
        while True:
            try:
                # 图片url
                image_url = self.image_queue.get(timeout=15)
                # 图片名
                image_name = image_url.split('/')[-1]
                # 保存路径
                save_path = os.path.join(SAVE_DIR, image_name)

                self.save_img(image_url, save_path)
            except (TimeoutError, queue.Empty):
                break

        return super(Module_Save, self).run()


def main():
    page_queue = queue.Queue(20)
    image_queue = queue.Queue(1000)
    for i in range(20):
        page_queue.put(URL.format(i * 24))

    for i in range(3):
        foo = Module_Spider(page_queue, image_queue, name=f'爬虫{i}号')
        foo.start()

    for i in range(3):
        foo = Module_Save(image_queue, name=f'保存{i}号')
        foo.start()


if __name__ == '__main__':
    main()
