#!/user/bin/env python
# 每天都要有好心情
import logging
import requests
import urllib3
import threading
import queue

from urllib3.exceptions import InsecureRequestWarning


class Module_Spider(threading.Thread):
    MSG_URL = 'https://api.live.bilibili.com/ajax/msg'

    def __init__(self, room_id: str, queue_data: queue.Queue, *args, **kwargs):
        # 房间号
        self.room_id = room_id
        # 数据队列
        self.data_queue = queue_data
        super(Module_Spider, self).__init__(*args, **kwargs)

    def run(self) -> None:
        """
        循环监听指定的房间
        :return:
        """
        while True:
            try:
                data = {
                    'roomid': self.room_id,
                    'csrf_token': '0222b660d74ad9fd581ad3cdb77e5262',
                    'csrf': '0222b660d74ad9fd581ad3cdb77e5262',
                    'visit_id': ''
                }
                resp = requests.post(Module_Spider.MSG_URL, data=data, verify=False)
                # 添加到数据队列中
                self.data_queue.put(resp.json()['data']['room'])
            except Exception as e:
                logging.error(self.name, e)


class Module_Parse(threading.Thread):
    def __init__(self, queue_data: queue.Queue, queue_barrage: queue.Queue, lock: threading.Lock, *args, **kwargs):
        # 数据队列
        self.data_queue = queue_data
        # 弹幕队列
        self.barrage_queue = queue_barrage
        # 锁
        self.lock = lock
        super(Module_Parse, self).__init__(*args, **kwargs)

    def parse(self, barrage):
        try:
            self.barrage_queue.put({
                'text': barrage['text'],  # 弹幕内容
                'nickname': barrage['nickname'],  # 发送者昵称
                'uid': barrage['uid'],  # 发送者id
                'timeline': barrage['timeline']  # 发送时间
            })
        except KeyError as e:
            logging.error(self.name, e)

    def run(self) -> None:
        global last_barrage

        while True:
            try:
                data_list = self.data_queue.get()

                for data in data_list:
                    if last_barrage:
                        # 判断弹幕数据是否已经保存过了,是则跳过
                        if data in last_barrage:
                            continue
                    self.parse(data)

                # 上锁
                self.lock.acquire()
                # 修改最后读取到的数据列表
                last_barrage = data_list
                # 解锁
                self.lock.release()
            except queue.Empty:
                pass


class Module_Save(threading.Thread):
    def __init__(self, queue_barrage: queue.Queue, *args, **kwargs):
        # 弹幕队列
        self.barrage_queue = queue_barrage
        super(Module_Save, self).__init__(*args, **kwargs)

    def run(self) -> None:
        while True:
            try:
                # 从队列中获取弹幕
                barrage = self.barrage_queue.get()
                print(f'[{barrage["timeline"]}] {barrage["nickname"]}:{barrage["text"]}')
            except queue.Empty:
                print('未捕捉到弹幕..')


if __name__ == '__main__':
    # 消除移除SSL验证的警告
    urllib3.disable_warnings(InsecureRequestWarning)
    # 数据队列
    data_queue = queue.Queue(1000)
    # 弹幕队列
    barrage_queue = queue.Queue(1000)
    # 最后获取的弹幕列表,用于处理重复数据
    last_barrage = None
    # 锁
    th_lock = threading.Lock()

    for i in range(2):
        foo = Module_Spider('7734200', data_queue, name=f'弹幕捕捉{i}号')
        foo.start()

    for i in range(2):
        foo = Module_Parse(data_queue, barrage_queue, th_lock, name=f'弹幕解析{i}号')
        foo.start()

    save_thread = Module_Save(barrage_queue, name='弹幕保存1号')
    save_thread.start()
