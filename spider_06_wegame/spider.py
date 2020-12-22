import requests
import json
import urllib3

from spider_06_wegame.config import *

urllib3.disable_warnings()  # 消除SSL认证警告


class Player:
    lol_id = None  # lol id
    lol_nick = None  # lol昵称
    lol_area = None  # 所在大区
    lol_head = None  # 游戏头像
    lol_rank = None  # rank


class Battle:
    bat_id = None  # 对局id
    bat_mode = None  # 对局模式
    bat_use_hero = None  # 使用英雄
    bat_kill = None  # 击杀数
    bat_death = None  # 死亡数
    bat_assist = None  # 助攻数
    bat_desc = None  # 对局备注
    bat_time = None  # 对局时间
    bat_score = None  # 对局评分
    is_win = None  # 胜负


class Spider_WeGame:
    def __init__(self):
        # 建立一个会话
        self.session = requests.Session()
        # 设置请求头
        self.session.headers = HEADERS
        # 这个与config中的qqinfo_ext->sig要一致
        self.session.cookies['skey'] = '@mMA8FM2jb'

    def login(self):
        # 登录请求url
        login_url = 'https://www.wegame.com.cn/api/middle/clientapi/auth/login_by_qq'
        # 请求登录
        self.session.post(login_url, data=json.dumps(LOGIN_DATA), verify=False)
        # 判断登录是否成功
        if self.session.cookies.get('tgp_ticket', None):
            self.session.headers.pop('Referer')  # 登录时需要用到,登录成功后就不需要了
            print('登录成功')
            print(self.session.cookies)
            return True
        else:
            return False

    def search_lol_user(self, nickname, area=None):
        search_url = 'https://m.wegame.com.cn/api/mobile/lua/proxy/index/mwg_lol_proxy/query_by_nick'
        # post请求需要的json数据
        data = {
            'search_nick': nickname
        }
        resp = self.session.post(search_url, data=json.dumps(data), verify=False).json()['data']['player_list']

        # 判断是否输入了大区
        area_key = None
        # 通过大区名找到大区id
        if area:
            foo = [k for k, v in LOL_GameArea.items() if v['name'] == area]
            try:
                area_key = int(foo[0])
            except IndexError:
                print('未找到对应大区..请查看是否输入有误')

        player_list = []
        for foo in resp:
            # 如果输入了大区,则只找对应大区的召唤师
            if area_key:
                if area_key != foo['area_id']:
                    continue

            player = Player()
            player.lol_id = foo['slol_id']  # 游戏id
            player.lol_nick = foo['game_nick']  # 游戏昵称
            player.lol_area = foo["area_id"]  # 游戏大区
            player.lol_rank = foo['rank_title']  # rank
            player.lol_head = foo['icon_url']  # 游戏头像
            player_list.append(player)

        return player_list

    def get_player_battle(self, player: Player, filter_type=0, limit=10):
        """
        查询玩家的最近对局
        :param player: 玩家
        :param filter_type: 查询类型 0:无筛选 1:匹配 2:排位 3:云顶
        :param limit: 查询数量
        :return:
        """
        url = 'https://m.wegame.com.cn/api/mobile/lua/proxy/index/mwg_lol_proxy/get_battle_list'
        # post请求所需数据
        data = {
            "offset": 0,  # 偏移量
            "limit": limit,  # 查询数量
            "filter_type": filter_type,  # 筛选条件 0:无 1:匹配 2:排位 3:云顶
            "totalNum": 0,
            "game_id": 26,
            "slol_id": player.lol_id,  # 召唤师id
            "area_id": player.lol_area,  # 所在大区
            "isMe": True
        }
        resp = self.session.post(url, data=json.dumps(data), verify=False).json()['data']

        result = []
        for battle_list in resp['player_battle_brief_list']:
            battle = Battle()
            try:
                battle.bat_id = battle_list["battle_id"]  # 对局id
                battle.bat_use_hero = LOL_Champion[str(battle_list["champion_id"])]  # 使用英雄
                battle.bat_mode = battle_list["game_mode_name"]  # 对局模式
                battle.bat_kill = battle_list['kill_num']  # 击杀数
                battle.bat_death = battle_list['death_num']  # 死亡数
                battle.bat_assist = battle_list['assist_num']  # 助攻数
                battle.bat_time = battle_list['battle_time']  # 对局时间 时间戳格式
                battle.bat_desc = battle_list['ext_tag_desc']  # 对局标签
                battle.bat_score = battle_list['game_score']  # 对局评分

                result.append(battle)
            except KeyError:
                pass

        return result

    def get_battle_detail(self, battle_id, player: Player):
        url = 'https://m.wegame.com.cn/api/mobile/lua/proxy/index/mwg_lol_proxy/get_battle_detail'
        # post请求所需数据
        data = {
            "game_id": 26,
            "dst_slol_id": player.lol_id,
            "req_slol_id": player.lol_id,
            "area_id": player.lol_area,
            "battle_id": battle_id,
        }
        battle_data = self.session.post(url, data=json.dumps(data), verify=False).json()['data']

    def run(self):
        if not self.login():
            return

        while True:
            keyword = input('请输入要查找的用户,输入格式(玩家昵称 所在大区), 大区可以不输入\n')
            print(*keyword.split(' '))
            players = self.search_lol_user(*keyword.split(' '))
            for player in players:
                print(f'玩家id:{player.lol_id}|玩家昵称:{player.lol_nick}|所在大区:{LOL_GameArea[str(player.lol_area)]["name"]}'
                      f'|段位:{player.lol_rank}')


if __name__ == '__main__':
    spider = Spider_WeGame()
    spider.run()
