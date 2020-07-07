#!/user/bin/env python
# 每天都要有好心情
from http.client import HTTPConnection
import json

from spider_05_BitTorrent.db import RedisClient

SAVE_PATH = 'E:/torrent/'
STOP_TIMEOUT = 60
MAX_CONCURRENT = 16
MAX_MAGNETS = 16

ARIA2RPC_ADDR = '127.0.0.1'
ARIA2RPC_PORT = 6800

rd = RedisClient()


def get_magnets():
    mg_list = rd.get_magnets(MAX_MAGNETS)
    for m in mg_list:
        yield m.decode()


def exec_rpc(magnet):
    conn = HTTPConnection(ARIA2RPC_ADDR, ARIA2RPC_PORT)
    req = {
        "jsonrpc": "2.0",
        "id": "magnet",
        "method": "aria2.addUri",
        "params": [
            [magnet],
            {
                "bt-stop-timeout": str(STOP_TIMEOUT),
                "max-concurrent-downloads": str(MAX_CONCURRENT),
                "listen-port": "6881",
                "dir": SAVE_PATH,
            },
        ],
    }
    conn.request(
        "POST", "/jsonrpc", json.dumps(req), {"Content-Type": "application/json"}
    )

    res = json.loads(conn.getresponse().read())
    if "error" in res:
        print("Aria2c replied with an error:", res["error"])


def magnet_torrent():
    for magnet in get_magnets():
        print('正在下载..', magnet)
        exec_rpc(magnet)


if __name__ == '__main__':
    magnet_torrent()
