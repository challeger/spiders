#!/user/bin/env python
# 每天都要有好心情

# 用于登录提交的json数据
LOGIN_DATA = {
    "login_info": {
        "qq_info_type": 6,
        "uin": "3436049981",
        # 这个字段应该是起到检验的作用,每次都会变,不过用登录时拿到的就可以了
        "sig": "MaxEvC4puzr4lE65J8HrH5JNQNFNvIpfsh9SZDXtxew_",
        'qqinfo_ext': [{
            'qq_info_type': 3,
            # 这个与cookie中的skey一致
            'sig': '',
        }]
    },
    "config_params": {
        "lang_type": 0
    },
    "mappid": "10001",
    "mcode": "",
    "clienttype": "1000005"
}
# 爬虫模拟请求头
HEADERS = {
    'Referer': 'https://www.wegame.com.cn/middle/login/third_callback.html',
    'Accept': 'application/json',
    'Accept-Encoding': 'application/json, text/plain, gzip',
    'User-Agent': 'okhttp/3.11.0',
    'Content-Type': 'application/json;charset=UTF-8',
}
# 我账号的LOL ID
SELF_LOL_ID = '9KJ3YaGWNx0'
# LOL英雄列表
LOL_Champion = {
    "1": {
        "id": "1",
        "ename": "Annie",
        "title": "黑暗之女",
        "cname": "安妮",
        "pic": "annie_square_0.png"
    },
    "2": {
        "id": "2",
        "ename": "Olaf",
        "title": "狂战士",
        "cname": "奥拉夫",
        "pic": "olaf_square_0.png"
    },
    "3": {
        "id": "3",
        "ename": "Galio",
        "title": "正义巨像",
        "cname": "加里奥",
        "pic": "galio_square_0.png"
    },
    "4": {
        "id": "4",
        "ename": "TwistedFate",
        "title": "卡牌大师",
        "cname": "崔斯特",
        "pic": "twistedfate_square_0.png"
    },
    "5": {
        "id": "5",
        "ename": "XinZhao",
        "title": "德邦总管",
        "cname": "赵信",
        "pic": "xinzhao_square_0.png"
    },
    "6": {
        "id": "6",
        "ename": "Urgot",
        "title": "无畏战车",
        "cname": "厄加特",
        "pic": "urgot_square_0.png"
    },
    "7": {
        "id": "7",
        "ename": "Leblanc",
        "title": "诡术妖姬",
        "cname": "乐芙兰",
        "pic": "leblanc_square_0.png"
    },
    "8": {
        "id": "8",
        "ename": "Vladimir",
        "title": "猩红收割者",
        "cname": "弗拉基米尔",
        "pic": "vladimir_square_0.png"
    },
    "9": {
        "id": "9",
        "ename": "FiddleSticks",
        "title": "远古恐惧",
        "cname": "费德提克",
        "pic": "fiddlesticks_square_0.png"
    },
    "10": {
        "id": "10",
        "ename": "Kayle",
        "title": "审判天使",
        "cname": "凯尔",
        "pic": "kayle_square_0.png"
    },
    "11": {
        "id": "11",
        "ename": "MasterYi",
        "title": "无极剑圣",
        "cname": "易",
        "pic": "masteryi_square_0.png"
    },
    "12": {
        "id": "12",
        "ename": "Alistar",
        "title": "牛头酋长",
        "cname": "阿利斯塔",
        "pic": "alistar_square_0.png"
    },
    "13": {
        "id": "13",
        "ename": "Ryze",
        "title": "符文法师",
        "cname": "瑞兹",
        "pic": "ryze_square_0.png"
    },
    "14": {
        "id": "14",
        "ename": "Sion",
        "title": "亡灵战神",
        "cname": "赛恩",
        "pic": "sion_square_0.png"
    },
    "15": {
        "id": "15",
        "ename": "Sivir",
        "title": "战争女神",
        "cname": "希维尔",
        "pic": "sivir_square_0.png"
    },
    "16": {
        "id": "16",
        "ename": "Soraka",
        "title": "众星之子",
        "cname": "索拉卡",
        "pic": "soraka_square_0.png"
    },
    "17": {
        "id": "17",
        "ename": "Teemo",
        "title": "迅捷斥候",
        "cname": "提莫",
        "pic": "teemo_square_0.png"
    },
    "18": {
        "id": "18",
        "ename": "Tristana",
        "title": "麦林炮手",
        "cname": "崔丝塔娜",
        "pic": "tristana_square_0.png"
    },
    "19": {
        "id": "19",
        "ename": "Warwick",
        "title": "祖安怒兽",
        "cname": "沃里克",
        "pic": "warwick_square_0.png"
    },
    "20": {
        "id": "20",
        "ename": "Nunu",
        "title": "雪原双子",
        "cname": "努努",
        "pic": "nunu_square_0.png"
    },
    "21": {
        "id": "21",
        "ename": "MissFortune",
        "title": "赏金猎人",
        "cname": "厄运小姐",
        "pic": "missfortune_square_0.png"
    },
    "22": {
        "id": "22",
        "ename": "Ashe",
        "title": "寒冰射手",
        "cname": "艾希",
        "pic": "ashe_square_0.png"
    },
    "23": {
        "id": "23",
        "ename": "Tryndamere",
        "title": "蛮族之王",
        "cname": "泰达米尔",
        "pic": "tryndamere_square_0.png"
    },
    "24": {
        "id": "24",
        "ename": "Jax",
        "title": "武器大师",
        "cname": "贾克斯",
        "pic": "jax_square_0.png"
    },
    "25": {
        "id": "25",
        "ename": "Morgana",
        "title": "堕落天使",
        "cname": "莫甘娜",
        "pic": "morgana_square_0.png"
    },
    "26": {
        "id": "26",
        "ename": "Zilean",
        "title": "时光守护者",
        "cname": "基兰",
        "pic": "zilean_square_0.png"
    },
    "27": {
        "id": "27",
        "ename": "Singed",
        "title": "炼金术士",
        "cname": "辛吉德",
        "pic": "singed_square_0.png"
    },
    "28": {
        "id": "28",
        "ename": "Evelynn",
        "title": "痛苦之拥",
        "cname": "伊芙琳",
        "pic": "evelynn_square_0.png"
    },
    "29": {
        "id": "29",
        "ename": "Twitch",
        "title": "瘟疫之源",
        "cname": "图奇",
        "pic": "twitch_square_0.png"
    },
    "30": {
        "id": "30",
        "ename": "Karthus",
        "title": "死亡颂唱者",
        "cname": "卡尔萨斯",
        "pic": "karthus_square_0.png"
    },
    "31": {
        "id": "31",
        "ename": "Chogath",
        "title": "虚空恐惧",
        "cname": "科'加斯",
        "pic": "chogath_square_0.png"
    },
    "32": {
        "id": "32",
        "ename": "Amumu",
        "title": "殇之木乃伊",
        "cname": "阿木木",
        "pic": "amumu_square_0.png"
    },
    "33": {
        "id": "33",
        "ename": "Rammus",
        "title": "披甲龙龟",
        "cname": "拉莫斯",
        "pic": "rammus_square_0.png"
    },
    "34": {
        "id": "34",
        "ename": "Anivia",
        "title": "冰晶凤凰",
        "cname": "艾尼维亚",
        "pic": "anivia_square_0.png"
    },
    "35": {
        "id": "35",
        "ename": "Shaco",
        "title": "恶魔小丑",
        "cname": "萨科",
        "pic": "shaco_square_0.png"
    },
    "36": {
        "id": "36",
        "ename": "DrMundo",
        "title": "祖安狂人",
        "cname": "蒙多医生",
        "pic": "drmundo_square_0.png"
    },
    "37": {
        "id": "37",
        "ename": "Sona",
        "title": "琴瑟仙女",
        "cname": "娑娜",
        "pic": "sona_square_0.png"
    },
    "38": {
        "id": "38",
        "ename": "Kassadin",
        "title": "虚空行者",
        "cname": "卡萨丁",
        "pic": "kassadin_square_0.png"
    },
    "39": {
        "id": "39",
        "ename": "Irelia",
        "title": "刀锋舞者",
        "cname": "艾瑞莉娅",
        "pic": "irelia_square_0.png"
    },
    "40": {
        "id": "40",
        "ename": "Janna",
        "title": "风暴之怒",
        "cname": "迦娜",
        "pic": "janna_square_0.png"
    },
    "41": {
        "id": "41",
        "ename": "Gangplank",
        "title": "海洋之灾",
        "cname": "普朗克",
        "pic": "gangplank_square_0.png"
    },
    "42": {
        "id": "42",
        "ename": "Corki",
        "title": "英勇投弹手",
        "cname": "库奇",
        "pic": "corki_square_0.png"
    },
    "43": {
        "id": "43",
        "ename": "Karma",
        "title": "天启者",
        "cname": "卡尔玛",
        "pic": "karma_square_0.png"
    },
    "44": {
        "id": "44",
        "ename": "Taric",
        "title": "瓦洛兰之盾",
        "cname": "塔里克",
        "pic": "taric_square_0.png"
    },
    "45": {
        "id": "45",
        "ename": "Veigar",
        "title": "邪恶小法师",
        "cname": "维迦",
        "pic": "veigar_square_0.png"
    },
    "48": {
        "id": "48",
        "ename": "Trundle",
        "title": "巨魔之王",
        "cname": "特朗德尔",
        "pic": "trundle_square_0.png"
    },
    "50": {
        "id": "50",
        "ename": "Swain",
        "title": "诺克萨斯统领",
        "cname": "斯维因",
        "pic": "swain_square_0.png"
    },
    "51": {
        "id": "51",
        "ename": "Caitlyn",
        "title": "皮城女警",
        "cname": "凯特琳",
        "pic": "caitlyn_square_0.png"
    },
    "53": {
        "id": "53",
        "ename": "Blitzcrank",
        "title": "蒸汽机器人",
        "cname": "布里茨",
        "pic": "blitzcrank_square_0.png"
    },
    "54": {
        "id": "54",
        "ename": "Malphite",
        "title": "熔岩巨兽",
        "cname": "墨菲特",
        "pic": "malphite_square_0.png"
    },
    "55": {
        "id": "55",
        "ename": "Katarina",
        "title": "不祥之刃",
        "cname": "卡特琳娜",
        "pic": "katarina_square_0.png"
    },
    "56": {
        "id": "56",
        "ename": "Nocturne",
        "title": "永恒梦魇",
        "cname": "魔腾",
        "pic": "nocturne_square_0.png"
    },
    "57": {
        "id": "57",
        "ename": "Maokai",
        "title": "扭曲树精",
        "cname": "茂凯",
        "pic": "maokai_square_0.png"
    },
    "58": {
        "id": "58",
        "ename": "Renekton",
        "title": "荒漠屠夫",
        "cname": "雷克顿",
        "pic": "renekton_square_0.png"
    },
    "59": {
        "id": "59",
        "ename": "JarvanIV",
        "title": "德玛西亚皇子",
        "cname": "嘉文四世",
        "pic": "jarvaniv_square_0.png"
    },
    "60": {
        "id": "60",
        "ename": "Elise",
        "title": "蜘蛛女皇",
        "cname": "伊莉丝",
        "pic": "elise_square_0.png"
    },
    "61": {
        "id": "61",
        "ename": "Orianna",
        "title": "发条魔灵",
        "cname": "奥莉安娜",
        "pic": "orianna_square_0.png"
    },
    "62": {
        "id": "62",
        "ename": "MonkeyKing",
        "title": "齐天大圣",
        "cname": "孙悟空",
        "pic": "monkeyking_square_0.png"
    },
    "63": {
        "id": "63",
        "ename": "Brand",
        "title": "复仇焰魂",
        "cname": "布兰德",
        "pic": "brand_square_0.png"
    },
    "64": {
        "id": "64",
        "ename": "LeeSin",
        "title": "盲僧",
        "cname": "李青",
        "pic": "leesin_square_0.png"
    },
    "67": {
        "id": "67",
        "ename": "Vayne",
        "title": "暗夜猎手",
        "cname": "薇恩",
        "pic": "vayne_square_0.png"
    },
    "68": {
        "id": "68",
        "ename": "Rumble",
        "title": "机械公敌",
        "cname": "兰博",
        "pic": "rumble_square_0.png"
    },
    "69": {
        "id": "69",
        "ename": "Cassiopeia",
        "title": "魔蛇之拥",
        "cname": "卡西奥佩娅",
        "pic": "cassiopeia_square_0.png"
    },
    "72": {
        "id": "72",
        "ename": "Skarner",
        "title": "水晶先锋",
        "cname": "斯卡纳",
        "pic": "skarner_square_0.png"
    },
    "74": {
        "id": "74",
        "ename": "Heimerdinger",
        "title": "大发明家",
        "cname": "黑默丁格",
        "pic": "heimerdinger_square_0.png"
    },
    "75": {
        "id": "75",
        "ename": "Nasus",
        "title": "沙漠死神",
        "cname": "内瑟斯",
        "pic": "nasus_square_0.png"
    },
    "76": {
        "id": "76",
        "ename": "Nidalee",
        "title": "狂野女猎手",
        "cname": "奈德丽",
        "pic": "nidalee_square_0.png"
    },
    "77": {
        "id": "77",
        "ename": "Udyr",
        "title": "兽灵行者",
        "cname": "乌迪尔",
        "pic": "udyr_square_0.png"
    },
    "78": {
        "id": "78",
        "ename": "Poppy",
        "title": "圣锤之毅",
        "cname": "波比",
        "pic": "poppy_square_0.png"
    },
    "79": {
        "id": "79",
        "ename": "Gragas",
        "title": "酒桶",
        "cname": "古拉加斯",
        "pic": "gragas_square_0.png"
    },
    "80": {
        "id": "80",
        "ename": "Pantheon",
        "title": "不屈之枪",
        "cname": "潘森",
        "pic": "pantheon_square_0.png"
    },
    "81": {
        "id": "81",
        "ename": "Ezreal",
        "title": "探险家",
        "cname": "伊泽瑞尔",
        "pic": "ezreal_square_0.png"
    },
    "82": {
        "id": "82",
        "ename": "Mordekaiser",
        "title": "金属大师",
        "cname": "莫德凯撒",
        "pic": "mordekaiser_square_0.png"
    },
    "83": {
        "id": "83",
        "ename": "Yorick",
        "title": "牧魂人",
        "cname": "约里克",
        "pic": "yorick_square_0.png"
    },
    "84": {
        "id": "84",
        "ename": "Akali",
        "title": "离群之刺",
        "cname": "阿卡丽",
        "pic": "akali_square_0.png"
    },
    "85": {
        "id": "85",
        "ename": "Kennen",
        "title": "狂暴之心",
        "cname": "凯南",
        "pic": "kennen_square_0.png"
    },
    "86": {
        "id": "86",
        "ename": "Garen",
        "title": "德玛西亚之力",
        "cname": "盖伦",
        "pic": "garen_square_0.png"
    },
    "89": {
        "id": "89",
        "ename": "Leona",
        "title": "曙光女神",
        "cname": "蕾欧娜",
        "pic": "leona_square_0.png"
    },
    "90": {
        "id": "90",
        "ename": "Malzahar",
        "title": "虚空先知",
        "cname": "玛尔扎哈",
        "pic": "malzahar_square_0.png"
    },
    "91": {
        "id": "91",
        "ename": "Talon",
        "title": "刀锋之影",
        "cname": "泰隆",
        "pic": "talon_square_0.png"
    },
    "92": {
        "id": "92",
        "ename": "Riven",
        "title": "放逐之刃",
        "cname": "锐雯",
        "pic": "riven_square_0.png"
    },
    "96": {
        "id": "96",
        "ename": "KogMaw",
        "title": "深渊巨口",
        "cname": "克格莫",
        "pic": "kogmaw_square_0.png"
    },
    "98": {
        "id": "98",
        "ename": "Shen",
        "title": "暮光之眼",
        "cname": "慎",
        "pic": "shen_square_0.png"
    },
    "99": {
        "id": "99",
        "ename": "Lux",
        "title": "光辉女郎",
        "cname": "拉克丝",
        "pic": "lux_square_0.png"
    },
    "101": {
        "id": "101",
        "ename": "Xerath",
        "title": "远古巫灵",
        "cname": "泽拉斯",
        "pic": "xerath_square_0.png"
    },
    "102": {
        "id": "102",
        "ename": "Shyvana",
        "title": "龙血武姬",
        "cname": "希瓦娜",
        "pic": "shyvana_square_0.png"
    },
    "103": {
        "id": "103",
        "ename": "Ahri",
        "title": "九尾妖狐",
        "cname": "阿狸",
        "pic": "ahri_square_0.png"
    },
    "104": {
        "id": "104",
        "ename": "Graves",
        "title": "法外狂徒",
        "cname": "格雷福斯",
        "pic": "graves_square_0.png"
    },
    "105": {
        "id": "105",
        "ename": "Fizz",
        "title": "潮汐海灵",
        "cname": "菲兹",
        "pic": "fizz_square_0.png"
    },
    "106": {
        "id": "106",
        "ename": "Volibear",
        "title": "不灭狂雷",
        "cname": "沃利贝尔",
        "pic": "volibear_square_0.png"
    },
    "107": {
        "id": "107",
        "ename": "Rengar",
        "title": "傲之追猎者",
        "cname": "雷恩加尔",
        "pic": "rengar_square_0.png"
    },
    "110": {
        "id": "110",
        "ename": "Varus",
        "title": "惩戒之箭",
        "cname": "韦鲁斯",
        "pic": "varus_square_0.png"
    },
    "111": {
        "id": "111",
        "ename": "Nautilus",
        "title": "深海泰坦",
        "cname": "诺提勒斯",
        "pic": "nautilus_square_0.png"
    },
    "112": {
        "id": "112",
        "ename": "Viktor",
        "title": "机械先驱",
        "cname": "维克托",
        "pic": "viktor_square_0.png"
    },
    "113": {
        "id": "113",
        "ename": "Sejuani",
        "title": "北地之怒",
        "cname": "瑟庄妮",
        "pic": "sejuani_square_0.png"
    },
    "114": {
        "id": "114",
        "ename": "Fiora",
        "title": "无双剑姬",
        "cname": "菲奥娜",
        "pic": "fiora_square_0.png"
    },
    "115": {
        "id": "115",
        "ename": "Ziggs",
        "title": "爆破鬼才",
        "cname": "吉格斯",
        "pic": "ziggs_square_0.png"
    },
    "117": {
        "id": "117",
        "ename": "Lulu",
        "title": "仙灵女巫",
        "cname": "璐璐",
        "pic": "lulu_square_0.png"
    },
    "119": {
        "id": "119",
        "ename": "Draven",
        "title": "荣耀行刑官",
        "cname": "德莱文",
        "pic": "draven_square_0.png"
    },
    "120": {
        "id": "120",
        "ename": "Hecarim",
        "title": "战争之影",
        "cname": "赫卡里姆",
        "pic": "hecarim_square_0.png"
    },
    "121": {
        "id": "121",
        "ename": "Khazix",
        "title": "虚空掠夺者",
        "cname": "卡兹克",
        "pic": "khazix_square_0.png"
    },
    "122": {
        "id": "122",
        "ename": "Darius",
        "title": "诺克萨斯之手",
        "cname": "德莱厄斯",
        "pic": "darius_square_0.png"
    },
    "126": {
        "id": "126",
        "ename": "Jayce",
        "title": "未来守护者",
        "cname": "杰斯",
        "pic": "jayce_square_0.png"
    },
    "127": {
        "id": "127",
        "ename": "Lissandra",
        "title": "冰霜女巫",
        "cname": "丽桑卓",
        "pic": "lissandra_square_0.png"
    },
    "131": {
        "id": "131",
        "ename": "Diana",
        "title": "皎月女神",
        "cname": "黛安娜",
        "pic": "diana_square_0.png"
    },
    "133": {
        "id": "133",
        "ename": "Quinn",
        "title": "德玛西亚之翼",
        "cname": "奎因",
        "pic": "quinn_square_0.png"
    },
    "134": {
        "id": "134",
        "ename": "Syndra",
        "title": "暗黑元首",
        "cname": "辛德拉",
        "pic": "syndra_square_0.png"
    },
    "136": {
        "id": "136",
        "ename": "AurelionSol",
        "title": "铸星龙王",
        "cname": "奥瑞利安索尔",
        "pic": "AurelionSol_Square_0.png"
    },
    "141": {
        "id": "141",
        "ename": "Kayn",
        "title": "影流之镰",
        "cname": "凯隐",
        "pic": "Kayn_Square_0.png"
    },
    "142": {
        "id": "142",
        "ename": "Zoe",
        "title": "暮光星灵",
        "cname": "佐伊",
        "pic": "Zoe_Square_0.png"
    },
    "143": {
        "id": "143",
        "ename": "Zyra",
        "title": "荆棘之兴",
        "cname": "婕拉",
        "pic": "zyra_square_0.png"
    },
    "145": {
        "id": "145",
        "ename": "Kaisa",
        "title": "虚空之女",
        "cname": "卡莎",
        "pic": "Kaisa_Square_0.png"
    },
    "150": {
        "id": "150",
        "ename": "Gnar",
        "title": "纳尔",
        "cname": "迷失之牙",
        "pic": "gnar_square_0.png"
    },
    "154": {
        "id": "154",
        "ename": "Zac",
        "title": "生化魔人",
        "cname": "扎克",
        "pic": "zac_square_0.png"
    },
    "157": {
        "id": "157",
        "ename": "Yasuo",
        "title": "疾风剑豪",
        "cname": "亚索",
        "pic": "yasuo_square_0.png"
    },
    "161": {
        "id": "161",
        "ename": "Velkoz",
        "title": "虚空之眼",
        "cname": "维克兹",
        "pic": "velkoz_square_0.png"
    },
    "163": {
        "id": "163",
        "ename": "Taliyah",
        "title": "岩雀",
        "cname": "塔莉垭",
        "pic": "Taliyah_Square_0.png"
    },
    "164": {
        "id": "164",
        "ename": "Camille",
        "title": "青钢影",
        "cname": "卡蜜尔",
        "pic": "Camille_Square_0.png"
    },
    "201": {
        "id": "201",
        "ename": "Braum",
        "title": "弗雷尔卓德之心",
        "cname": "布隆",
        "pic": "braum_square_0.png"
    },
    "202": {
        "id": "202",
        "ename": "Jhin",
        "title": "戏命师",
        "cname": "烬",
        "pic": "Jhin_Square_0.png"
    },
    "203": {
        "id": "203",
        "ename": "Kindred",
        "title": "永猎双子",
        "cname": "千珏",
        "pic": "Kindred_Square_0.png"
    },
    "222": {
        "id": "222",
        "ename": "Jinx",
        "title": "暴走萝莉",
        "cname": "金克丝",
        "pic": "jinx_square_0.png"
    },
    "223": {
        "id": "223",
        "ename": "TahmKench",
        "title": "河流之王",
        "cname": "塔姆",
        "pic": "TahmKench_Square_0.png"
    },
    "235": {
        "id": "235",
        "ename": "Seanna",
        "title": "涤魂圣枪",
        "cname": "赛娜",
        "pic": "Seanna_Square_0.png"
    },
    "236": {
        "id": "236",
        "ename": "Lucian",
        "title": "圣枪游侠",
        "cname": "卢锡安",
        "pic": "lucian_square_0.png"
    },
    "238": {
        "id": "238",
        "ename": "Zed",
        "title": "影流之主",
        "cname": "劫",
        "pic": "zed_square_0.png"
    },
    "240": {
        "id": "240",
        "ename": "Kled",
        "title": "暴怒骑士",
        "cname": "克烈",
        "pic": "Kled_Splash_0.png"
    },
    "245": {
        "id": "245",
        "ename": "Ekko",
        "title": "时间刺客",
        "cname": "艾克",
        "pic": "Ekko_Square_0.png"
    },
    "246": {
        "id": "246",
        "ename": "Qiyana",
        "title": "元素女皇",
        "cname": "奇亚娜",
        "pic": "Qiyana_Square_0.png"
    },
    "254": {
        "id": "254",
        "ename": "Vi",
        "title": "皮城执法官",
        "cname": "蔚",
        "pic": "vi_square_0.png"
    },
    "266": {
        "id": "266",
        "ename": "Aatrox",
        "title": "暗裔剑魔",
        "cname": "亚托克斯",
        "pic": "aatrox_square_0.png"
    },
    "267": {
        "id": "267",
        "ename": "Nami",
        "title": "唤潮鲛姬",
        "cname": "娜美",
        "pic": "nami_square_0.png"
    },
    "268": {
        "id": "268",
        "ename": "Azir",
        "title": "沙漠皇帝",
        "cname": "阿兹尔",
        "pic": "azir_square_0.png"
    },
    "350": {
        "id": "350",
        "ename": "Yuumi",
        "title": "悠米",
        "cname": "悠米",
        "pic": "Yuumi_Square_0.png"
    },
    "412": {
        "id": "412",
        "ename": "Thresh",
        "title": "魂锁典狱长",
        "cname": "锤石",
        "pic": "thresh_square_0.png"
    },
    "420": {
        "id": "420",
        "ename": "Illaoi",
        "title": "海兽祭司",
        "cname": "俄洛伊",
        "pic": "illaoi_Square_0.png"
    },
    "421": {
        "id": "421",
        "ename": "RekSai",
        "title": "虚空遁地兽",
        "cname": "雷克塞",
        "pic": "RekSai.png"
    },
    "427": {
        "id": "427",
        "ename": "Ivern",
        "title": "翠神",
        "cname": "艾翁",
        "pic": "Ivern_Square_0.png"
    },
    "429": {
        "id": "429",
        "ename": "Kalista",
        "title": "复仇之矛",
        "cname": "卡莉丝塔",
        "pic": "Kalista.png"
    },
    "432": {
        "id": "432",
        "ename": "Bard",
        "title": "星界游神",
        "cname": "巴德",
        "pic": "Bard_Square_0.png"
    },
    "497": {
        "id": "497",
        "ename": "Rakan",
        "title": "幻翎",
        "cname": "洛",
        "pic": "Rakan_Square_0.png"
    },
    "498": {
        "id": "498",
        "ename": "Xayah",
        "title": "逆羽",
        "cname": "霞",
        "pic": "Xayah_Square_0.png"
    },
    "516": {
        "id": "516",
        "ename": "Ornn",
        "title": "山隐之焰",
        "cname": "奥恩",
        "pic": "Ornn_Square_0.png"
    },
    "517": {
        "id": "517",
        "ename": "Sylas",
        "title": "解脱者",
        "cname": "塞拉斯",
        "pic": "Sylas_Square_0.png"
    },
    "518": {
        "id": "518",
        "ename": "Neeko",
        "title": "万花通灵",
        "cname": "妮蔻",
        "pic": "Neeko_Square_0.png"
    },
    "523": {
        "id": "523",
        "ename": "Aphelios",
        "title": "残月之肃",
        "cname": "厄斐琉斯",
        "pic": "Aphelios_Square_0.png"
    },
    "555": {
        "id": "555",
        "ename": "Pyke",
        "title": "血港鬼影",
        "cname": "派克",
        "pic": "Pyke_Square_0.png"
    },
    "875": {
        "id": "875",
        "ename": "Sett",
        "title": "腕豪",
        "cname": "瑟提",
        "pic": "Sett_Square_0.png"
    }
}
# LOL大区列表
LOL_GameArea = {
    "1": {
        "id": "1",
        "strid": "HN1",
        "isp": "电信一",
        "name": "艾欧尼亚",
    },
    "3": {
        "id": "3",
        "strid": "HN2",
        "isp": "电信二",
        "name": "祖安",
    },
    "4": {
        "id": "4",
        "strid": "HN3",
        "isp": "电信三",
        "name": "诺克萨斯",
    },
    "2": {
        "id": "2",
        "strid": "WT1",
        "isp": "网通一",
        "name": "比尔吉沃特",
    },
    "6": {
        "id": "6",
        "strid": "WT2",
        "isp": "网通二",
        "name": "德玛西亚",
    },
    "9": {
        "id": "9",
        "strid": "WT3",
        "isp": "网通三",
        "name": "弗雷尔卓德",
    },
    "5": {
        "id": "5",
        "strid": "HN4",
        "isp": "电信四",
        "name": "班德尔城",
    },
    "7": {
        "id": "7",
        "strid": "HN5",
        "isp": "电信五",
        "name": "皮尔特沃夫",
    },
    "8": {
        "id": "8",
        "strid": "HN6",
        "isp": "电信六",
        "name": "战争学院",
    },
    "10": {
        "id": "10",
        "strid": "HN7",
        "isp": "电信七",
        "name": "巨神峰",
    },
    "11": {
        "id": "11",
        "strid": "HN8",
        "isp": "电信八",
        "name": "雷瑟守备",
    },
    "12": {
        "id": "12",
        "strid": "WT4",
        "isp": "网通四",
        "name": "无畏先锋",
    },
    "17": {
        "id": "17",
        "strid": "HN12",
        "isp": "电信十二",
        "name": "钢铁烈阳",
    },
    "13": {
        "id": "13",
        "strid": "HN9",
        "isp": "电信九",
        "name": "裁决之地",
    },
    "14": {
        "id": "14",
        "strid": "HN10",
        "isp": "电信十",
        "name": "黑色玫瑰",
    },
    "15": {
        "id": "15",
        "strid": "HN11",
        "isp": "电信十一",
        "name": "暗影岛",
    },
    "16": {
        "id": "16",
        "strid": "WT5",
        "isp": "网通五",
        "name": "恕瑞玛",
    },
    "19": {
        "id": "19",
        "strid": "HN14",
        "isp": "电信十四",
        "name": "均衡教派",
    },
    "18": {
        "id": "18",
        "strid": "HN13",
        "isp": "电信十三",
        "name": "水晶之痕",
    },
    "20": {
        "id": "20",
        "strid": "WT6",
        "isp": "网通六",
        "name": "扭曲丛林",
    },
    "21": {
        "id": "21",
        "strid": "EDU1",
        "isp": "教育网",
        "name": "教育网专区",
    },
    "22": {
        "id": "22",
        "strid": "HN15",
        "isp": "电信十五",
        "name": "影流",
    },
    "23": {
        "id": "23",
        "strid": "HN16",
        "isp": "电信十六",
        "name": "守望之海",
    },
    "24": {
        "id": "24",
        "strid": "HN17",
        "isp": "电信十七",
        "name": "征服之海",
    },
    "25": {
        "id": "25",
        "strid": "HN18",
        "isp": "电信十八",
        "name": "卡拉曼达",
    },
    "26": {
        "id": "26",
        "strid": "WT7",
        "isp": "网通七",
        "name": "巨龙之巢",
    },
    "27": {
        "id": "27",
        "strid": "HN19",
        "isp": "电信十九",
        "name": "皮城警备",
    },
    "30": {
        "id": "30",
        "strid": "BGP1",
        "isp": "全网络大区一",
        "name": "男爵领域",
        "ob": "0"
    },
    "31": {
        "id": "31",
        "strid": "BGP2",
        "isp": "全网络大区二",
        "name": "峡谷之巅",
    }
}
# LOL段位列表
LOL_TIER = ("最强王者", "钻石", "铂金", "黄金", "白银", "青铜", "超凡大师", "傲世宗师", "黑铁")
# LOL小段列表
TIER_LEVEL = ("Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ")
# LOL游戏模式
GAME_MODE = {
    "1": "匹配赛",
    "2": "人机",
    "3": "灵活排位",
    "4": "排位赛",
    "5": "灵活排位",
    "6": "大乱斗",
    "7": "匹配赛",
    "8": "自定义",
    "9": "统治战场",
    "10": "新手指导",
    "11": "克隆赛",
    "12": "大对决",
    "13": "大对决",
    "14": "无限火力",
    "15": "镜像赛",
    "16": "末日赛",
    "17": "飞升赛",
    "18": "六杀丛林",
    "19": "魄罗乱斗",
    "20": "互选征召",
    "21": "佣兵战",
    "22": "新统治",
    "23": "枢纽攻防",
    "24": "无限乱斗",
    "25": "提莫人机",
    "26": "红月决",
    "27": "重开局",
    "28": "峡谷大乱斗",
    "29": "死兆星",
    "30": "怪兽入侵",
    "31": "过载",
    "32": "冰雪火力",
    "33": "冠军赛",
    "34": "极限闪击",
    "35": "奥德赛"
}
