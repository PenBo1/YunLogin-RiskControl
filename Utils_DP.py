import time
from logging import exception
import asyncio
from multiprocessing.dummy import current_process
from random import randint
from traceback import print_tb
import os
import requests
import json
import random
import string
import shutil
from DrissionPage import Chromium, ChromiumOptions
from openpyxl.styles.builtins import title
from logger import log_info, log_debug, log_warning, log_error  # 新增logger导入


class browerUtils():
    def __init__(self, url="", log=True, rate: float = 0.08):
        """
        click_ads_rate 广告点击几率

        :param url:
        :param log:
        :param click_ads_rate:
        """
        self.url = None
        self.task_id = None
        self.page = None
        self.browser = None
        self.ws = None
        self.log = log
        self.rng = random.Random()
        self.clkads = False  # 是否点击过广告

        if self.rng.random() < rate: #是否点击广告点击
            self.set_click_ads = True#点击广告
        else:
            self.set_click_ads = False

        # for i in range(0, 5):
        #     if self.getIp() != "":
        #         break
        # if self.PublicIP == "":
        #     return
        code = self.createBrower(url)
        try:

            code = json.loads(code)
            self.id = code["data"]["browse"][0]["id"]
            code = self.startBrower()
            code = json.loads(code)
            self.ws = code["data"]["ws"]["selenium"]
            
        except Exception as e:
            # print("browerUtils error", e)
            log_error(f"browerUtils error: {e}")
            self.deleteBrower()
            return

    def deleteBrower(self):
        # 创建浏览器时得ID
        list = {
            "browserid": [self.id]
        }
        try:
            # 发送 GET 请求
            response = requests.post("http://localhost:50213/api/v2/userapi/user/delete", json.dumps(list))
            # self.log and print("deleteBrower Status Code:", response.status_code)
            log_info(f"deleteBrower Status Code: {response.status_code}")
            log_info(f"deleteBrower response.text: {response.text}")
            self.deleteBrowerPath()
            return response.text
        except requests.exceptions.RequestException as e:
            log_info(f"deleteBrower An error occurred: {e}")
    def deleteBrowerPath(self):
        folder_path = r"E:\.YunLogin\User Data\Shop-" + self.id

        if os.path.exists(folder_path):
            try:
                shutil.rmtree(folder_path)
                log_info(f"文件夹 {folder_path} 已删除！")
                # print(f"文件夹 {folder_path} 已删除！")
            except Exception as e:
                log_info(f"删除文件夹时出错：{e}")
                # print("删除文件夹失败",e)
    def createBrower(self, url=""):
        # socks5 = self.proxy
        # https = {
        #     "Addr": "gate-hk.kkoip.com:16586",
        #     "User": "4412679-3737a568-US-session-24511258",
        #     "Passwd": "3871a960"
        # }
        data = {
            "browser": [
                {
                    "name": "YunLogin-风控测试环境",
                    "proxy": {
                        "uuid": "",
                        "PublicIP": "",  # 获取IP
                        "type": "local",
                        "region": "US"
                    },
                    "accounts": {
                        "openurls": [url],
                        "groupid": "",
                        "cookie": ""
                    },
                    "accountsv2": [
                        {
                            "url": "",
                            "password": "",
                            "user": ""
                        }
                    ],
                    "finger": {  # random.choice(["107", "119", "122"])
                        "kernelversion": "127",
                        "System": "All Windows",
                        "Language": ["en-US"],
                        "Zone": "",
                        "WebRTC": 2,
                        "Canvas": 2,
                        "WebGl": 0,
                        "dpi": "随机",
                        "AudioContext": 1,
                        "MediaDevice": 2,
                        "Hardware": 1,
                        "Bluetooth": 1,
                        "DoNotTrack": 1,
                        "EnableScanPort": 1,
                        "ScanPort": [155],
                        "geographic": {
                            "enable": 1,
                            "useip": 1
                        },
                        "Cpu" : 24,
                        "Mem" : 8
                    },

                }
            ]
        }
        log_info(f"createBrower data: {data}")  # 使用log_info代替print
        try:
            # 发送 GET 请求
            response = requests.post("http://localhost:50213/api/v2/userapi/user/create", json.dumps(data))
            # self.log and print("response.text:", response.text)
            log_info(f"createBrower response.status_code: {response.status_code}")
            log_info(f"createBrower response.text: {response.text}")
            return response.text
        except requests.exceptions.RequestException as e:
            log_info(f"createBrower An error occurred: {e}")
            # print(f"An error occurred: {e}")

    def stopBrower(self):
        try:
            # 发送 GET 请求
            response = requests.get("http://localhost:50213/api/v2/browser/stop?account_id=" + self.id)
            # self.log and print("stopBrower   Status Code:", response.status_code)
            log_info(f"stopBrower Status Code: {response.status_code}")
            log_info(f"stopBrower response.text: {response.text}")
            return response.text
        except requests.exceptions.RequestException as e:
            log_info(f"stopBrower An error occurred: {e}")
            # print(f"An error occurred: {e}")

    def startBrower(self):
        try:
            # 发送 GET 请求
            response = requests.get("http://localhost:50213/api/v2/browser/start?account_id=" + self.id)
            # self.log and print("startBrower response.text:", response.text)
            log_info(f"startBrower response.status_code: {response.status_code}")
            log_info(f"startBrower response.text: {response.text}")
            return response.text
        except requests.exceptions.RequestException as e:
            # print(f"An error occurred: {e}")
            log_info(f"startBrower An error occurred: {e}")

    def generate_random_string(self, length):
        characters = string.ascii_letters + string.digits  # 包含字母和数字
        return ''.join(random.choice(characters) for _ in range(length))

    def getIp(self):
        ip = ""
        try:

            proxy = {
                "Addr": "gate-hk.kkoip.com:16586",
                "User": "4412679-3737a568-US-session-" + str(random.randint(100000000, 999999999)),
                "Passwd": "3871a960",
                "PublicIP": ""
            }
            self.proxy = proxy

            proxy = {
                "http": f"http://{proxy['User']}:{proxy['Passwd']}@{proxy['Addr']}",
                "https": f"http://{proxy['User']}:{proxy['Passwd']}@{proxy['Addr']}",
            }
            try:
                response = requests.get("http://xiaopang.sto.ipidea.online/", proxies=proxy, timeout=3)
                data = json.loads(response.text)
                ip = data["ip"]
                self.PublicIP = ip
            except Exception as e:
                log_error(f"getIp Error: {e}")
            # print(response.text)
            # print(f"PublicIP: {ip}")
            log_info(f"PublicIP: {ip}")
            return ip
        except exception as e:
            # self.log and print("getIp Error", e)
            log_error(f"getIp Error: {e}")
        return ""

    def connect(self, task_id, url):
        self.url = url
        self.task_id = task_id
        if self.ws == "":
            # print(f"task_id:{self.task_id} 创建浏览器失败")
            log_error(f"task_id:{self.task_id} 创建浏览器失败")
            return
        # 需要创建一个浏览器并且 获取到 wss链接
        try:
            co = ChromiumOptions().set_timeouts(page_load=35, script=35, base=35)

            browser = Chromium(self.ws, co)

        except  Exception as e:
            # print(f"task_id:{self.task_id} 连接浏览器失败 Error:{e}")
            log_error(f"task_id:{self.task_id} 创建浏览器失败 Error:{e}")
            self.stopBrower()  # 停止浏览器
            self.deleteBrower()  # 删除浏览器
            return

        page = browser.get_tabs()
        self.page = page[0]
        self.browser = browser

        time.sleep(15)
        try:
            #self.page.get(self.rand_ref_url(), timeout=30)  # 设置超时时间为 30 秒
            self.getAutomationAttributes()  # 获取浏览器的自动化属性
            self.getFingerprint()  # 获取浏览器指纹信息
            self.page.get(self.url, timeout=30)  # 设置超时时间为 30 秒
            log_info(f"task_id:{self.task_id} 打开页面 {self.url}")
            self.page.wait.doc_loaded()
            # print("等待DOM加载完毕")
            log_info("等待DOM加载完毕")
            time.sleep(30)
            # self.page.run_js(f"""
            # var a = document.createElement("a");
            #     a.href = "{self.url}";
            #     a.target = '_self';
            #     document.body.append(a);
            #     a.click()
            # """)
            self.page.wait.doc_loaded()
            self.page.set.activate()

        except  Exception as e:
            # print(f"task_id:{self.task_id} Error", e)
            self.browser.quit()
            self.deleteBrower()  # 删除浏览器
            return False  # 退出当前任务
        return True
    
    def getAutomationAttributes(self):
        """
        获取浏览器的自动化属性
        """
        properties = [
    "navigator.webdriver",
    "window._phantom",
    "window.callPhantom",
    "window.__nightmare",
    "window.__phantomas",
    "window.emit",
    "window.spawn",
    "window.clientInformation.webdriver",
    "window.webdriver",
    "window.navigator.webdriver",
    "window.domAutomation",
    "window.domAutomationController",
    "window._WEBDRIVER_ELEM_CACHE",
    "document.documentElement.getAttribute('webdriver')",
    "window._Selenium_IDE_Recorder",
    "document.__webdriver_script_fn",
    "document.documentElement.getAttribute('webdriver')",
    "document.documentElement.getAttribute('selenium')",
    "document.documentElement.getAttribute('driver')",
    "document.__webdriver_evaluate",
    "document.__selenium_evaluate",
    "document.__webdriver_script_function",
    "document.__webdriver_script_func",
    "document.__webdriver_script_fn",
    "document.__fxdriver_evaluate",
    "document.__driver_unwrapped",
    "document.__webdriver_unwrapped",
    "document.__driver_evaluate",
    "document.__selenium_unwrapped",
    "document.__fxdriver_unwrapped",
    "window.external.toString().indexOf('Sequentum') != -1",
    "Object.keys(window.document).filter(k=>k.match(/\\$[a-z]dc_/) && window.document[k].cache_)"
]
        
        results = {}
        for prop in properties:
            try:
                value = self.page.run_js(f"return {prop};")
                results[prop] = value
                log_info(f"检测浏览器自动化属性 {prop}: {value}")
            except Exception as e:
                log_error(f"Error getting {prop}: {e}")
        
        return results

    def getFingerprint(self):
        """
        获取浏览器指纹信息
        """
        # 创建浏览器时得ID
        list = {
            "browserid": [self.id]
        }
        try:
            # 发送 GET 请求
            response = requests.post("http://localhost:50213/api/v2/userapi/user/list", json.dumps(list))
            # self.log and print("deleteBrower Status Code:", response.status_code)
            log_info(f"BrowerFingerprint Status Code: {response.status_code}")
            log_info(f"BrowerFingerprin response.text: {response.text}")

        except requests.exceptions.RequestException as e:
            log_info(f"BrowerFingerprin An error occurred: {e}")
