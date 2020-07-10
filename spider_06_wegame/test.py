import requests
import time
import json
import urllib3


urllib3.disable_warnings()  # 消除SSL认证警告
print(time.strftime('%X', time.gmtime(1594206725)))
tt = time.gmtime(1594206725)
print(f'{tt.tm_mon}-{tt.tm_mday} {tt.tm_hour + 8}:{tt.tm_min}')
# data = {
#     "login_info": {
#         "qq_info_type": 3,
#         "uin": "3436049981",
#         "sig": "@E1agHItdr"
#     },
#     "config_params": {
#         "lang_type": 0
#     },
#     "mappid": "10001",
#     "mcode": "",
#     "clienttype": "1000005"
# }
# headers = {
#     'Referer': 'https://www.wegame.com.cn/middle/login/third_callback.html',
#     'Accept-Encoding': 'application/json, text/plain, gzip',
#     'User-Agent': 'okhttp/3.11.0',
#     'Content-Type': 'application/json;charset=UTF-8',
# }
# session = requests.Session()
# session.headers = headers
# url = 'https://www.wegame.com.cn/api/middle/clientapi/auth/login_by_qq'
# session.post(url, data=json.dumps(data), verify=False)  # 模拟登录
#
# nickname = input('输入角色昵称:')
#
# data_1 = {
#     'search_nick': nickname
# }
# url = 'https://m.wegame.com.cn/api/mobile/lua/proxy/index/mwg_lol_proxy/query_by_nick'
# resp = session.post(url, data=json.dumps(data_1), verify=False).json()
# print(resp)
# url_1 = 'https://m.wegame.com.cn/api/mobile/lua/wegame_bizsvr/do_search_user'
# url_2 = 'https://m.wegame.com.cn/api/mobile/lua/wegameapp_lsvr/get_user_role_cards'
# resp = requests.post(url_1, headers=headers, data=json.dumps(data), verify=False).json()['data']['info_list'][0]
# print(resp)
# print(f'查询QQ:{qq}\n用户昵称:{resp["nick"]}\n用户id: {resp["uid"]}')
# data_role = {
#     'dst': resp["uid"]
# }
# resp2 = requests.post(url_2, headers=headers, verify=False, data=json.dumps(data_role)).json()['data']['all_game_role_cards'][0]['one_game_role_cards'][0]['role']
# print(f'角色名:{resp2["role_name"]}\n角色id:{resp2["role_id"]}')

# data_lol = {
#     'game_id': 26,
#     'slol_id': resp2['role_id'],
#     'area_id': resp2['area_id']
# }

# url_3 = 'https://m.wegame.com.cn/api/mobile/lua/proxy/index/mwg_lol_proxy/get_battle_topbar_info'
# resp3 = requests.post(url_3, headers=headers, verify=False, data=json.dumps(data_lol))
# print(resp3.json())
