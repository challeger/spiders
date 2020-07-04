#!/user/bin/env python
# 每天都要有好心情
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

"""
使用selenium模拟登录,搜索,点击播放按钮使其返回歌曲信息的json数据,
抓取模块进行抓取
"""


class Spider_163:
    def __init__(self, account, password):
        self.account = account
        self.password = password
        self.isLogin = False

    def init(self):
        self.ops = Options()
        self.ops.add_argument('--proxy-server=http://localhost:8080')  # 设置代理,方便监听
        self.browser = webdriver.Chrome(chrome_options=self.ops)
        self.wait = WebDriverWait(self.browser, 10)  # 隐性等待10s

    def login(self):
        print('正在登陆....')
        try:
            url = 'https://music.163.com/'
            self.browser.get(url)

            login_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.link.s-fc3'))
            )  # 登录按钮
            login_btn.click()

            other_login_way = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.u-btn2.other'))
            )  # 其他方式登录按钮
            sleep(1)
            other_login_way.click()

            agree_select = self.wait.until(
                EC.element_to_be_clickable((By.ID, 'j-official-terms'))
            )  # 同意xx政策
            agree_select.click()

            phone_login = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.u-btn2.u-btn2-2'))
            )  # 手机号登录按钮
            sleep(1)
            phone_login.click()

            phone_input = self.wait.until(
                EC.presence_of_element_located((By.ID, 'p'))
            )  # 手机号输入框
            password_input = self.wait.until(
                EC.presence_of_element_located((By.ID, 'pw'))
            )  # 密码输入框
            submit_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.j-primary.u-btn2.u-btn2-2'))
            )  # 登录按钮

            sleep(1.5)
            phone_input.send_keys(self.account)  # 输入账号
            sleep(1.5)
            password_input.send_keys(self.password)  # 输入密码
            sleep(1.5)
            submit_btn.click()

            user_head = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.head.f-fl.f-pr'))
            )  # 用户头像,判断是否登录成功
            print('登录成功')
            self.isLogin = True

        except TimeoutException:
            print('登录超时')

    def search(self, keyword):
        if not self.isLogin:
            self.login()
        try:
            url = 'https://music.163.com/'
            self.browser.get(url)

            search_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#srch'))
            )  # 搜索框
            search_input.send_keys(keyword)
            sleep(1)
            search_input.send_keys(Keys.ENTER)

            sleep(5)  # 等待页面跳转与加载
            self.browser.switch_to.frame('g_iframe')  # 切换到内嵌html页面
            play_btn_list = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.hd a'))
            )  # 所有播放按钮
            for btn in play_btn_list[:5]:
                btn.click()
                sleep(5)
        except TimeoutException:
            print('搜索失败')
