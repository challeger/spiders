#!/user/bin/env python
# 每天都要有好心情
import socket
import codecs
import time
from multiprocessing import Process
from threading import Thread

from bencoder import bencode, bdecode
from collections import deque

from spider_05_BitTorrent.utils import *
from spider_05_BitTorrent.db import RedisClient

# 服务器 tracker
DHT_NODES = [
    ("67.215.246.10", 6881),
    ("82.221.103.244", 6881),
    ("23.21.224.150", 6881),
    ("93.158.213.92", 1337),
    ("188.241.58.209", 6969),
]

# 双端队列容量
MAX_NODE_SIZE = 10000
# UDP报文 buff size
UDP_RECV_BUFFSIZE = 65535
# 服务 host
SERVER_HOST = '0.0.0.0'
# 服务 port
SERVER_PORT = 9090
# 磁力链接前缀
MAGENT_PER = 'magnet:?xt=urn:btih:{}'
# while 循环休眠时间
SLEEP_TIME = 1e-5
# 节点 id 长度
PER_NID_LEN = 20
# 执行 bs 定时器间隔（秒）
PER_SEC_BS_TIMER = 8
# 进程数
MAX_PROCESSES = 4


class HNode:
    def __init__(self, nid, ip=None, port=None):
        self.nid = nid
        self.ip = ip
        self.port = port


class DHTServer:
    def __init__(self, bind_ip, bind_port):
        self.bind_ip = bind_ip
        self.bind_port = bind_port
        self.nid = get_rand_id()
        # nodes节点是一个双端队列
        self.nodes = deque(maxlen=MAX_NODE_SIZE)
        # KRPC协议是由bencode编码组成的一个简单的PRC结构, 使用UDP报文发送
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.udp.bind((self.bind_ip, self.bind_port))
        self.redis = RedisClient()

    def join_DHT(self):
        print('尝试加入DHT网络')
        for address in DHT_NODES:
            self.send_find_node(address)

    def send_krpc(self, msg, address):
        try:
            self.udp.sendto(bencode(msg), address)
        except Exception as e:
            print(e)

    def send_find_node(self, address, nid=None):
        """

        :param address: 地址元组(ip, port)
        :param nid: 节点id
        """
        nid = get_neighbor(nid, self.nid) if nid else self.nid
        tid = get_rand_id()  # 生成一个伪装的id
        msg = dict(
            t=tid,  # 请求节点的id
            y='q',  # 消息的类型 q->请求 r->回复 e->错误
            q='find_node',  # 指定请求为find_node
            a=dict(id=nid, target=get_rand_id()),  # 请求所带的参数
        )
        self.send_krpc(msg, address)

    def find_nodes(self):
        while True:
            try:
                # 弹出一个节点
                node = self.nodes.popleft()
                self.send_find_node((node.ip, node.port), node.nid)
                time.sleep(SLEEP_TIME)
            except IndexError:
                # 节点队列为空,重新加入DHT网络
                self.join_DHT()

    def bs_timer(self):
        """
        定时执行join_DHT()
        :return:
        """
        t = 1
        while True:
            if t % PER_SEC_BS_TIMER == 0:
                t = 1
                self.join_DHT()
            t += 1
            time.sleep(1)

    def on_message(self, msg, address):
        try:
            if msg[b'y'] == b'r':
                if msg[b'r'].get(b'nodes', None):
                    self.on_find_node_response(msg)
            elif msg[b'y'] == b'q':
                if msg[b'q'] == b'get_peers':
                    self.on_get_peers_request(msg, address)
                elif msg[b'q'] == b'announce_peer':
                    self.on_announce_peer_request(msg, address)
        except KeyError:
            pass

    def save_magnet(self, info_hash):
        hex_info_hash = codecs.getencoder('hex')(info_hash)[0].decode()
        magent = MAGENT_PER.format(hex_info_hash)
        print(f'获取到磁力链接{magent}')
        self.redis.add_magent(magent)

    def receive_response(self):
        self.join_DHT()
        while True:
            try:
                # 接收返回报文
                data, address = self.udp.recvfrom(UDP_RECV_BUFFSIZE)
                # 解码返回的数据
                msg = bdecode(data)
                # 处理返回的信息
                self.on_message(msg, address)
                time.sleep(SLEEP_TIME)
            except Exception as e:
                print(e)

    def on_find_node_response(self, msg):
        nodes = get_nodes_info(msg[b'r'][b'nodes'])
        for node in nodes:
            nid, ip, port = node
            if len(nid) != PER_NID_LEN or ip == self.bind_ip:
                continue
            self.nodes.append(HNode(nid, ip, port))

    def on_get_peers_request(self, msg, address):
        tid = msg[b't']
        try:
            info_hash = msg[b'a'][b'info_hash']
            self.save_magnet(info_hash)
        except KeyError:
            print('没有info hash')

    def on_announce_peer_request(self, msg, address):
        tid = msg[b't']
        try:
            info_hash = msg[b'a'][b'info_hash']
            self.save_magnet(info_hash)
        except KeyError:
            print('没有info hash')


def _start_thread(offset):
    """
    启动线程

    :param offset: 端口偏移值
    """
    dht = DHTServer(SERVER_HOST, SERVER_PORT + offset)
    threads = [
        Thread(target=dht.receive_response),
        Thread(target=dht.find_nodes),
        Thread(target=dht.bs_timer),
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()


def start_server():
    """
    多线程启动服务
    """
    processes = []
    _start_thread(1)
    for i in range(MAX_PROCESSES):
        processes.append(Process(target=_start_thread, args=(i,)))

    for p in processes:
        p.start()

    for p in processes:
        p.join()


if __name__ == '__main__':
    start_server()
