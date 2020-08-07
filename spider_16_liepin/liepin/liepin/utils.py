import requests
import threading
import datetime
import time


class Proxy:
    def __init__(self, api):
        super().__init__()
        # 获取代理的api链接
        self.api = api
        # 获得的代理地址
        self.proxy_url = None
        # 代理的过期时间
        self.expire_time = None
        # 代理是否被拉入黑名单
        self.is_blacked = True
        # 用来进行代理的更换
        self.th = threading.Thread(target=self.update_proxy)

        self.th.start()

    def get_proxy(self):
        """
        获取新的代理
        """
        try:
            data = requests.get(self.api).json()['data'][0]
        except IndexError:
            return
        self.proxy_url = f"https://{data['ip']}:{data['port']}"
        self.expire_time = datetime.datetime.strptime(data['expire_time'], '%Y-%m-%d %H:%M:%S')
        self.is_blacked = False
        print(f'获取了新的代理:{self.proxy_url}')

    @property
    def is_expiring(self):
        """
        判断代理是否超时
        """
        now = datetime.datetime.now()
        return (self.expire_time - now) <= datetime.timedelta(seconds=5)

    def check_proxy(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
        }

        resp = requests.get(url, headers=headers, proxies={
            'https': self.proxy_url
        })
        if resp.status_code != 200:
            self.is_blacked = True

    def update_proxy(self):
        """
        当代理超时或者被拉黑时,更新代理
        """
        while True:
            time.sleep(1)
            if self.is_blacked or self.is_expiring:
                self.get_proxy()
